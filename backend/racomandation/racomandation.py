import json
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

class ArtRecommender:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = None
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.user_preferences = {}
        self.user_preferences_file_image = {}
        self.artwork_features = {}
        self.is_classifier_trained = {}  # Track training status for each user
        self.preferences_file = os.path.join(os.getcwd(), 'racomandation/user_preferences.json')
        self._load_preferences()  # Load existing preferences on initialization
        
    def _load_preferences(self):
        """Load user preferences from JSON file if it exists"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r') as file:
                    self.user_preferences = json.load(file)
                # Convert user preferences to include artwork features
                for user_id, preferences in self.user_preferences.items():
                    self.user_preferences_file_image[user_id] = {
                        'liked': [],
                        'disliked': []
                    }
                    
                    # Load artwork features from json file
                    artwork_features_file = os.path.join(os.getcwd(), 'racomandation/artwork_features.json')
                    with open(artwork_features_file, 'r') as file:
                        artwork_data = json.load(file)
                    
                    # Process liked images
                    if 'liked' in preferences:
                        for image_name in preferences['liked']:
                            if image_name in artwork_data:
                                self.user_preferences_file_image[user_id]['liked'].append({
                                    'file_name': image_name,
                                    'file_data': artwork_data[image_name]
                                })
                                
                    # Process disliked images            
                    if 'disliked' in preferences:
                        for image_name in preferences['disliked']:
                            if image_name in artwork_data:
                                self.user_preferences_file_image[user_id]['disliked'].append({
                                    'file_name': image_name,
                                    'file_data': artwork_data[image_name]
                                })
                    
                print(f"Loaded preferences for {len(self.user_preferences)} users")
        except Exception as e:
            print(f"Error loading preferences: {e}")
            self.user_preferences = {}

    def _save_preferences(self):
        """Save user preferences to JSON file"""
        try:
            with open(self.preferences_file, 'w') as file:
                json.dump(self.user_preferences, file, indent=2)
            print("Preferences saved successfully")
        except Exception as e:
            print(f"Error saving preferences: {e}")

    def process_artwork_features(self, artwork_data):
        """
        Process artwork features (colors, style, composition, etc.)
        
        Parameters:
        artwork_data: dict with artwork_id as key and features as values
        """
        if not artwork_data:
            raise ValueError("No artwork data provided")
            
        features = np.array(list(artwork_data.values()))
        n_samples, n_features = features.shape
        
        # Normalize features
        features_scaled = self.scaler.fit_transform(features)
        
        # Initialize PCA with appropriate number of components
        n_components = min(n_samples, n_features, 64)
        self.pca = PCA(n_components=n_components)
        
        # Reduce dimensionality
        features_reduced = self.pca.fit_transform(features_scaled)
        
        # Store processed features
        for idx, art_id in enumerate(artwork_data.keys()):
            self.artwork_features[art_id] = features_reduced[idx]
                    
        print(f"Processed {len(artwork_data)} artworks. Feature dimension reduced from {n_features} to {n_components}")
    
    def record_swipe(self, user_id, artwork_id, liked):
        """
        Record user's swipe action (like/dislike)
        """
        if not self.artwork_features:
            raise ValueError("No artwork features processed. Call process_artwork_features first.")
            
        if artwork_id not in self.artwork_features:
            raise ValueError(f"Artwork ID {artwork_id} not found in processed features")
            
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {'liked': [], 'disliked': []}
            self.is_classifier_trained[user_id] = False
        
        if liked:
            self.user_preferences[user_id]['liked'].append(artwork_id)
        else:
            self.user_preferences[user_id]['disliked'].append(artwork_id)
            
        # Save preferences after each update
        self._save_preferences()
            
        # Train classifier if enough data is available
        self._train_classifier(user_id)
    
    def _train_classifier(self, user_id):
        """
        Train a classifier based on user's likes and dislikes
        """
        liked_count = len(self.user_preferences[user_id]['liked'])
        disliked_count = len(self.user_preferences[user_id]['disliked'])
        
        print(f"User {user_id} has {liked_count} likes and {disliked_count} dislikes")
        
        # Skip training if not enough data
        if liked_count < 5 or disliked_count < 5:
            self.is_classifier_trained[user_id] = False
            return
        
        # Prepare training data
        X = []
        y = []
        
        # Add liked artworks
        for art_id in self.user_preferences[user_id]['liked']:
            if art_id in self.artwork_features:
                X.append(self.artwork_features[art_id])
                y.append(1)
                
        # Add disliked artworks
        for art_id in self.user_preferences[user_id]['disliked']:
            if art_id in self.artwork_features:
                X.append(self.artwork_features[art_id])
                y.append(0)
        
        # Train classifier
        X = np.array(X)
        y = np.array(y)
        self.classifier.fit(X, y)
        self.is_classifier_trained[user_id] = True
        
        print(f"Trained classifier for user {user_id} with {len(X)} samples")
    
    def get_recommendations(self, user_id, n_recommendations=10):
        """
        Get artwork recommendations for a user
        
        Parameters:
        user_id: unique identifier for the user
        n_recommendations: number of recommendations to return
        
        Returns:
        list of artwork IDs sorted by predicted preference
        """        
        if not self.artwork_features:
            raise ValueError("No artwork features processed. Call process_artwork_features first.")
        
        # If user has no preferences or classifier isn't trained, use similarity-based approach
        if (user_id not in self.user_preferences or 
            not self.is_classifier_trained.get(user_id, False)):
            print(f"Using similarity-based recommendations for user {user_id}")
            return self._get_similarity_based_recommendations(user_id, n_recommendations)
        
        print(f"Using classifier-based recommendations for user {user_id}")
        # Use trained classifier for predictions
        predictions = {}
        for art_id, features in self.artwork_features.items():
            if art_id not in self.user_preferences[user_id]['liked'] and \
               art_id not in self.user_preferences[user_id]['disliked']:
                pred_prob = self.classifier.predict_proba(features.reshape(1, -1))[0][1]
                predictions[art_id] = pred_prob
        
        # Sort artworks by predicted probability and return top N
        recommended_arts = sorted(
            predictions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [art_id for art_id, _ in recommended_arts[:n_recommendations]]
    
    def _get_similarity_based_recommendations(self, user_id, n_recommendations):
        """
        Get recommendations based on similarity to liked artworks
        """
        # If user has no preferences, return random recommendations
        if user_id not in self.user_preferences or not self.user_preferences[user_id]['liked']:
            print(f"No preferences found for user {user_id}, returning random recommendations")
            all_arts = list(self.artwork_features.keys())
            np.random.shuffle(all_arts)
            return all_arts[:n_recommendations]
        
        # Calculate average feature vector of liked artworks
        liked_features = []
        for art_id in self.user_preferences[user_id]['liked']:
            if art_id in self.artwork_features:
                liked_features.append(self.artwork_features[art_id])
        
        user_profile = np.mean(liked_features, axis=0)
        
        # Calculate similarity scores
        similarities = {}
        for art_id, features in self.artwork_features.items():
            if art_id not in self.user_preferences[user_id]['liked'] and \
               art_id not in self.user_preferences[user_id]['disliked']:
                similarity = cosine_similarity(
                    user_profile.reshape(1, -1),
                    features.reshape(1, -1)
                )[0][0]
                similarities[art_id] = similarity
        
        # Sort artworks by similarity and return top N
        recommended_arts = sorted(
            similarities.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [art_id for art_id, _ in recommended_arts[:n_recommendations]]


# Example usage
def example_usage(recommender):
    # Initialize recommender
    # Load JSON from a file
    print(os.getcwd())
    with open(os.path.join(os.getcwd(), 'racomandation/artwork_features.json'), 'r') as file:
        data = json.load(file)
    
    artwork_features = data
    
    # Process artwork features
    recommender.process_artwork_features(artwork_features)
    
    # Simulate user swipes
    user_id = 'user1'
    
    # Get recommendations
    recommendations = recommender.get_recommendations(user_id)
        
    return {"recommendations": recommendations}
