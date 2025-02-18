import csv
import json
import os
from flask import Flask
from racomandation.main import ArtRecommender, example_usage
app = Flask(__name__)

@app.route("/")
def hello_world():

    return example_usage()



@app.route("/api/swipe")
def recommendations():
        # Initialize recommender
    # Load JSON from a file
    print(os.getcwd())
    with open(os.path.join(os.getcwd(), 'racomandation/artwork_features.json'), 'r') as file:
        data = json.load(file)

    recommender = ArtRecommender()
    
    artwork_features = data
    
    # Process artwork features
    recommender.process_artwork_features(artwork_features)
    
    # Simulate user swipes
    user_id = 'user1'
    recommender.record_swipe(user_id, 'image_242.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_422.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_215.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_12.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_220.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_110.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_283.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_145.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_150.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_289.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_161.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_492.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_255.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_321.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_364.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_136.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_119.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_245.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_193.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_299.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_163.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_156.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_229.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_274.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_268.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_478.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_423.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_330.jpg', liked=False)
    recommender.record_swipe(user_id, 'image_453.jpg', liked=True)
    recommender.record_swipe(user_id, 'image_142.jpg', liked=True)
    
    # Get recommendations
    recommendations = recommender.get_recommendations(user_id)
    
        
    return {"recommendations": recommendations}


@app.route("/api/test/recommendations")
def recommendations_test():
        # Open and read the metadata CSV file
    metadata = []
    try:
        with open('/Users/luisbeqja/Desktop/Personal Projects/TindeArt/wikiart_images/metadata.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                metadata.append(row)
    except FileNotFoundError:
        return "Metadata file not found", 404
    except Exception as e:
        return f"Error reading metadata: {str(e)}", 500
    
    # Get recommendations from example_usage
    recommendations_data = example_usage()
    
    # Create a mapping of filenames to metadata
    metadata_map = {row['filename']: row for row in metadata}
    
    # Get full metadata for each recommended artwork
    enriched_recommendations = []
    for filename in recommendations_data['recommendations']:
        if filename in metadata_map:
            artwork_info = {
                'filename': filename,
                'artist': metadata_map[filename]['artist'],
                'genre': metadata_map[filename]['genre'], 
                'style': metadata_map[filename]['style'],
            }
            enriched_recommendations.append(artwork_info)
    
    return {'recommendations': enriched_recommendations}