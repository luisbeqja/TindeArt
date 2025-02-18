import numpy as np
from PIL import Image
import os
from sklearn.cluster import KMeans
from collections import Counter

class ImageFeatureExtractor:
    def __init__(self, n_colors=5, hist_bins=8):
        """
        Initialize the feature extractor
        
        Parameters:
        n_colors: number of dominant colors to extract
        hist_bins: number of bins for color histogram
        """
        self.n_colors = n_colors
        self.hist_bins = hist_bins
        
    def extract_features(self, image_path):
        """
        Extract features from an image
        
        Parameters:
        image_path: path to the image file
        
        Returns:
        feature_vector: numpy array of features
        """
        # Load and resize image
        img = Image.open(image_path)
        img = img.convert('RGB')
        img = img.resize((150, 150))  # Resize for consistency
        img_array = np.array(img)
        
        # Extract different types of features
        color_features = self._extract_color_features(img_array)
        histogram_features = self._extract_histogram_features(img_array)
        composition_features = self._extract_composition_features(img_array)
        
        # Combine all features
        feature_vector = np.concatenate([
            color_features,
            histogram_features,
            composition_features
        ])
        
        return feature_vector
    
    def _extract_color_features(self, img_array):
        """Extract dominant colors and color statistics"""
        # Reshape the image array for k-means
        pixels = img_array.reshape(-1, 3)
        
        # Find dominant colors using k-means
        kmeans = KMeans(n_clusters=self.n_colors, n_init=10)
        kmeans.fit(pixels)
        
        # Get the dominant colors and their proportions
        colors = kmeans.cluster_centers_
        labels = kmeans.labels_
        color_counts = Counter(labels)
        total_pixels = sum(color_counts.values())
        
        # Calculate color proportions
        color_props = [count/total_pixels for count in color_counts.values()]
        
        # Calculate mean and std for each channel
        means = img_array.mean(axis=(0, 1)) / 255.0
        stds = img_array.std(axis=(0, 1)) / 255.0
        
        # Combine color features
        color_features = np.concatenate([
            means,  # 3 features
            stds,   # 3 features
            color_props  # n_colors features
        ])
        
        return color_features
    
    def _extract_histogram_features(self, img_array):
        """Extract color histogram features"""
        histograms = []
        
        # Calculate histogram for each channel
        for channel in range(3):
            hist, _ = np.histogram(
                img_array[:, :, channel],
                bins=self.hist_bins,
                range=(0, 256),
                density=True
            )
            histograms.extend(hist)
        
        return np.array(histograms)
    
    def _extract_composition_features(self, img_array):
        """Extract image composition features"""
        features = []
        
        # Split image into regions (3x3 grid)
        height, width = img_array.shape[:2]
        h_split = height // 3
        w_split = width // 3
        
        # Calculate brightness for each region
        for i in range(3):
            for j in range(3):
                region = img_array[
                    i*h_split:(i+1)*h_split,
                    j*w_split:(j+1)*w_split
                ]
                brightness = region.mean() / 255.0
                features.append(brightness)
        
        # Add overall brightness and contrast
        features.append(img_array.mean() / 255.0)  # Overall brightness
        features.append(img_array.std() / 255.0)   # Overall contrast
        
        return np.array(features)
    
    def process_directory(self, directory_path):
        """
        Process all images in a directory
        
        Parameters:
        directory_path: path to directory containing images
        
        Returns:
        artwork_features: dictionary of image features
        """
        artwork_features = {}
        
        for filename in os.listdir(directory_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(directory_path, filename)
                try:
                    features = self.extract_features(image_path)
                    artwork_features[filename] = features
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")
        
        return artwork_features

# Example usage
def example_usage():
    # Initialize feature extractor
    extractor = ImageFeatureExtractor()
    
    # Extract features from a single image
    image_path = "../client/src/assets/art/monalisa.jpg"
    features = extractor.extract_features(image_path)
    print(f"Extracted {len(features)} features from image")
    
    # Or process an entire directory
    directory_path = "../client/src/assets/art/"
    artwork_features = extractor.process_directory(directory_path)
    print(f"Processed {artwork_features} images")
    
    return artwork_features

if __name__ == "__main__":
    example_usage()