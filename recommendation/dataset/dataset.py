from datasets import load_dataset
import os
import csv
from PIL import Image

# Load dataset in streaming mode
dataset = load_dataset("huggan/wikiart", split="train", streaming=True)

# Create output directories
output_folder = "wikiart_images"
os.makedirs(output_folder, exist_ok=True)

# Metadata file
metadata_path = os.path.join(output_folder, "metadata.csv")

# Open CSV file for writing metadata
with open(metadata_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["filename", "artist", "genre", "style", "title"])  # CSV header

    # Loop through dataset and save only first 500 images
    for idx, item in enumerate(dataset):
        if idx >= 500:  # Stop after saving 500 images
            break

        # Save image
        image = item["image"]
        filename = f"image_{idx}.jpg"
        image_path = os.path.join(output_folder, filename)
        image.save(image_path, "JPEG")
        
        filename = f"image_{idx}.jpg"
        # Save metadata
        print(item)
        csv_writer.writerow([
            filename,
            item['image'],
            item['genre'],
            item['style'],
        ])

        if idx % 100 == 0:
            print(f"Saved {idx} images...")

print(f"Finished! 500 images and metadata saved in '{output_folder}'")
