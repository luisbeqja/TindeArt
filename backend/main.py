import csv
import json
import os
from flask import Flask, request
from racomandation.racomandation import ArtRecommender, example_usage
from flask_cors import CORS
from utils import format_recommendations

app = Flask(__name__)
recommender = ArtRecommender()


with open(os.path.join(os.getcwd(), 'racomandation/artwork_features.json'), 'r') as file:
    data = json.load(file)

artwork_features = data
    
# Process artwork features
recommender.process_artwork_features(artwork_features)


CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def hello_world():
    return example_usage()


@app.route("/api/user_preferences")
def user_preferences():
    return recommender.user_preferences



@app.route("/api/swipe")
def handle_swipe():
    # Get query parameters
    userid = request.args.get('userid')
    image = request.args.get('image')
    liked = request.args.get('liked').lower() == 'true'  # Convert string to boolean

    # Record user swipe
    recommender.record_swipe(userid, image, liked=liked)
    # Get recommendations
    recommendations = recommender.get_recommendations(userid)
    # Format and return recommendations
    return format_recommendations({"recommendations": recommendations})

@app.route("/api/recommendations")
def get_recommendations():    
    return format_recommendations(example_usage(recommender))