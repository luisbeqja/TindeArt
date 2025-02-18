# Art Recommender System Documentation

## Overview
The Art Recommender System is a Python-based recommendation engine designed for a Tinder-like art application. It learns user preferences through swipe actions (like/dislike) and provides personalized art recommendations using a combination of machine learning techniques.

## Class: ArtRecommender

### Constructor
```python
recommender = ArtRecommender()
```
Initializes a new instance of the art recommendation system with:
- StandardScaler for feature normalization
- Dynamic PCA for dimensionality reduction
- RandomForestClassifier for learning user preferences
- Storage for user preferences and artwork features

### Core Methods

#### process_artwork_features(artwork_data)
```python
recommender.process_artwork_features(artwork_data)
```
Processes and stores artwork features for use in recommendations.

**Parameters:**
- `artwork_data`: Dictionary where:
  - Keys: Artwork IDs (strings)
  - Values: Feature vectors (lists/arrays of numerical values)

**Functionality:**
1. Normalizes features using StandardScaler
2. Reduces dimensionality using PCA
3. Stores processed features for each artwork

**Example:**
```python
artwork_features = {
    'art1': [0.8, 0.2, 0.3, 0.5],
    'art2': [0.3, 0.7, 0.4, 0.6]
}
recommender.process_artwork_features(artwork_features)
```

#### record_swipe(user_id, artwork_id, liked)
```python
recommender.record_swipe(user_id, artwork_id, liked)
```
Records a user's swipe action on an artwork.

**Parameters:**
- `user_id`: Unique identifier for the user (string)
- `artwork_id`: Identifier for the artwork (string)
- `liked`: Boolean indicating if the user liked (True) or disliked (False) the artwork

**Functionality:**
1. Creates user preference profile if it doesn't exist
2. Records the swipe action
3. Triggers classifier training if enough data is available

**Example:**
```python
recommender.record_swipe('user123', 'art1', liked=True)
```

#### get_recommendations(user_id, n_recommendations=10)
```python
recommendations = recommender.get_recommendations(user_id, n_recommendations=10)
```
Generates personalized artwork recommendations for a user.

**Parameters:**
- `user_id`: Unique identifier for the user (string)
- `n_recommendations`: Number of recommendations to return (integer, default=10)

**Returns:**
- List of artwork IDs sorted by predicted preference

**Functionality:**
1. For new users (<2 likes): Uses similarity-based recommendations
2. For established users: Uses trained classifier predictions

**Example:**
```python
recommended_arts = recommender.get_recommendations('user123', n_recommendations=5)
```

### Helper Methods

#### _train_classifier(user_id)
Internal method that trains the RandomForestClassifier on user preferences.

**Functionality:**
1. Collects liked and disliked artwork features
2. Trains classifier when user has at least 2 likes and 2 dislikes
3. Used for making predictions in get_recommendations

#### _get_similarity_based_recommendations(user_id, n_recommendations)
Internal method for generating recommendations based on feature similarity.

**Functionality:**
1. Calculates average feature vector of liked artworks
2. Computes cosine similarity with other artworks
3. Returns most similar artworks not yet seen by user

## Implementation Example

```python
# Initialize the recommender
recommender = ArtRecommender()

# Process artwork features
artwork_features = {
    'art1': [0.8, 0.2, 0.3, 0.5],
    'art2': [0.3, 0.7, 0.4, 0.6],
    'art3': [0.5, 0.5, 0.5, 0.5]
}
recommender.process_artwork_features(artwork_features)

# Record user interactions
user_id = 'user123'
recommender.record_swipe(user_id, 'art1', liked=True)
recommender.record_swipe(user_id, 'art2', liked=False)

# Get recommendations
recommendations = recommender.get_recommendations(user_id)
```

## Error Handling

The system includes various error checks:
1. Validates artwork data before processing
2. Ensures artwork features are processed before recording swipes
3. Validates artwork IDs when recording swipes
4. Handles cases with insufficient data for recommendations

## Best Practices

1. **Feature Processing:**
   - Process all artwork features before recording any user interactions
   - Ensure feature vectors are consistent in size
   - Use normalized numerical values for features

2. **User Interactions:**
   - Record all user swipes to improve recommendation quality
   - Handle both positive (likes) and negative (dislikes) feedback
   - Maintain consistent user IDs across sessions

3. **Recommendations:**
   - Request recommendations after recording sufficient user interactions
   - Adjust n_recommendations based on your application's needs
   - Handle cases where recommendations might be empty

## Technical Requirements

Required Python packages:
- numpy
- scikit-learn

## Performance Considerations

1. **Memory Usage:**
   - Artwork features are stored in memory
   - User preferences are stored in memory
   - Consider implementing database storage for large-scale applications

2. **Processing Time:**
   - Feature processing is done once per artwork
   - Classifier training occurs after sufficient user interactions
   - Recommendation generation scales with artwork collection size