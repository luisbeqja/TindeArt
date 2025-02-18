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
        self.artwork_features = {}
        self.is_classifier_trained = {}  # Track training status for each user
        
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
            
        # Train classifier if enough data is available
        self._train_classifier(user_id)
    
    def _train_classifier(self, user_id):
        """
        Train a classifier based on user's likes and dislikes
        """
        liked_count = len(self.user_preferences[user_id]['liked'])
        disliked_count = len(self.user_preferences[user_id]['disliked'])
        
        print(f"User {user_id} has {liked_count} likes and {disliked_count} dislikes")
        
        if liked_count < 2 or disliked_count < 2:
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
    
    def get_recommendations(self, user_id, n_recommendations=1):
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
def example_usage():
    # Initialize recommender
    recommender = ArtRecommender()
    
    artwork_features = {
    'Girl-With-A-Pearl-Earring-Wallpaper-Mural-88792671': [1.54601656e-01, 1.26957037e-01, 1.07204706e-01, 2.33639751e-01,
       1.98521130e-01, 1.48729456e-01, 6.73066667e-01, 1.16622222e-01,
       8.20000000e-02, 8.12888889e-02, 4.70222222e-02, 2.12666667e-02,
       2.08611111e-03, 1.79722222e-03, 1.95138889e-03, 2.08333333e-03,
       1.18611111e-03, 7.68055556e-04, 1.11111111e-04, 2.15777778e-02,
       3.01805556e-03, 1.95277778e-03, 2.09722222e-03, 1.49166667e-03,
       8.90277778e-04, 1.66666667e-04, 5.55555556e-05, 2.34569444e-02,
       2.71666667e-03, 2.64861111e-03, 1.19583333e-03, 8.72222222e-04,
       3.02777778e-04, 5.69444444e-05, 0.00000000e+00, 2.61322876e-02,
       1.58451242e-01, 1.79205229e-02, 1.20729935e-01, 2.94654641e-01,
       1.08575686e-01, 5.30917647e-02, 2.83860392e-01, 1.02873725e-01,
       1.29587800e-01, 1.97696940e-01], 
    'the-scheam': [4.80077211e-01, 3.42788671e-01, 2.13826405e-01, 2.81155079e-01,
       2.07345776e-01, 1.35384469e-01, 1.01200000e-01, 1.92888889e-01,
       1.67600000e-01, 2.36488889e-01, 3.01822222e-01, 5.42361111e-03,
       3.95416667e-03, 2.85972222e-03, 3.22638889e-03, 3.40694444e-03,
       4.82638889e-03, 6.25833333e-03, 1.29444444e-03, 5.96111111e-03,
       5.69027778e-03, 6.15972222e-03, 6.33333333e-03, 3.69861111e-03,
       2.26388889e-03, 1.11944444e-03, 2.36111111e-05, 7.64166667e-03,
       1.41625000e-02, 5.82222222e-03, 2.12222222e-03, 9.65277778e-04,
       4.98611111e-04, 3.75000000e-05, 0.00000000e+00, 4.64153725e-01,
       4.68770196e-01, 4.19902222e-01, 3.56604967e-01, 3.25300392e-01,
       2.74499869e-01, 3.59383007e-01, 1.66509281e-01, 2.74953203e-01,
       3.45564096e-01, 2.42092065e-01], 
    'monalisa': [3.39758954e-01, 2.85584837e-01, 2.13285577e-01, 2.10560665e-01,
       2.05743859e-01, 9.15014822e-02, 2.17022222e-01, 2.07555556e-01,
       1.99955556e-01, 2.89155556e-01, 8.63111111e-02, 5.30694444e-03,
       7.25277778e-03, 6.13333333e-03, 5.27361111e-03, 4.24583333e-03,
       1.62500000e-03, 8.75000000e-04, 5.37500000e-04, 9.84027778e-03,
       6.08194444e-03, 4.80416667e-03, 4.05277778e-03, 4.55416667e-03,
       1.55972222e-03, 3.56944444e-04, 0.00000000e+00, 4.20000000e-03,
       1.73708333e-02, 7.44583333e-03, 2.22083333e-03, 1.25000000e-05,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 4.15665882e-01,
       3.63990065e-01, 4.25539869e-01, 2.63842614e-01, 3.20436601e-01,
       2.44462222e-01, 1.81514248e-01, 1.82875294e-01, 1.17561307e-01,
       2.79543123e-01, 1.85374721e-01], 
    'Portrait_of_Jeanne_Modigliani': [5.47412810e-01, 3.84798606e-01, 2.38740741e-01, 3.09805137e-01,
       2.15757811e-01, 1.39617705e-01, 2.34222222e-01, 1.27733333e-01,
       3.00977778e-01, 1.33288889e-01, 2.03777778e-01, 5.53611111e-03,
       2.48888889e-03, 1.84305556e-03, 1.05555556e-03, 3.75277778e-03,
       6.06666667e-03, 6.37916667e-03, 4.12777778e-03, 5.91666667e-03,
       3.64722222e-03, 4.83472222e-03, 7.08055556e-03, 4.98055556e-03,
       3.38194444e-03, 1.40277778e-03, 5.55555556e-06, 7.81250000e-03,
       9.48611111e-03, 8.75972222e-03, 3.84027778e-03, 1.10000000e-03,
       2.51388889e-04, 0.00000000e+00, 0.00000000e+00, 5.12737255e-01,
       3.17637647e-01, 4.06341961e-01, 4.56976209e-01, 5.03813856e-01,
       3.85593203e-01, 2.83603660e-01, 4.60640523e-01, 1.85512157e-01,
       3.90317386e-01, 2.64391546e-01], 
    'dali-the-persistence-of-memory': [4.72823007e-01, 4.51763137e-01, 3.46183529e-01, 2.02859879e-01,
       2.58452207e-01, 2.38794887e-01, 9.16444444e-02, 2.17066667e-01,
       1.98888889e-01, 3.59866667e-01, 1.32533333e-01, 1.38888889e-06,
       4.71666667e-03, 7.84444444e-03, 6.29027778e-03, 3.36111111e-03,
       5.03611111e-03, 3.92083333e-03, 7.91666667e-05, 5.13888889e-05,
       1.06527778e-02, 5.30972222e-03, 2.37916667e-03, 3.28750000e-03,
       3.12500000e-03, 5.15416667e-03, 1.29027778e-03, 1.12777778e-03,
       1.57583333e-02, 3.69027778e-03, 1.80277778e-03, 2.72916667e-03,
       2.75416667e-03, 3.16250000e-03, 2.25000000e-04, 6.31270065e-01,
       6.61562876e-01, 5.80664052e-01, 3.94211242e-01, 3.85797647e-01,
       2.85899085e-01, 3.80945359e-01, 3.04406797e-01, 1.87551895e-01,
       4.23589891e-01, 2.40957844e-01], 
    'The_Starry_Night_Van_Gogh': [3.37530632e-01, 4.49046100e-01, 4.94876863e-01, 2.56955587e-01,
       2.49511984e-01, 2.17306829e-01, 2.02666667e-01, 2.42177778e-01,
       2.49822222e-01, 1.64666667e-01, 1.40666667e-01, 5.23194444e-03,
       1.16944444e-02, 4.44027778e-03, 2.71805556e-03, 1.95833333e-03,
       1.58472222e-03, 1.48333333e-03, 2.13888889e-03, 3.36111111e-03,
       5.13472222e-03, 4.75694444e-03, 5.08750000e-03, 4.42083333e-03,
       3.73472222e-03, 3.08888889e-03, 1.66527778e-03, 1.05555556e-03,
       5.53750000e-03, 2.69444444e-03, 4.38888889e-03, 6.77777778e-03,
       7.65972222e-03, 2.95416667e-03, 1.81944444e-04, 4.60095686e-01,
       5.12841830e-01, 5.78703791e-01, 4.10354510e-01, 5.74905621e-01,
       5.29579608e-01, 2.04378562e-01, 3.18540654e-01, 2.54960523e-01,
       4.27151198e-01, 2.50734029e-01]}
    
    # Process artwork features
    recommender.process_artwork_features(artwork_features)
    
    # Simulate user swipes
    user_id = 'user1'
    recommender.record_swipe(user_id, 'Portrait_of_Jeanne_Modigliani', liked=True)
    recommender.record_swipe(user_id, 'Girl-With-A-Pearl-Earring-Wallpaper-Mural-88792671', liked=True)
    recommender.record_swipe(user_id, 'the-scheam', liked=True)
    recommender.record_swipe(user_id, 'The_Starry_Night_Van_Gogh', liked=False)
    
    # Get recommendations
    recommendations = recommender.get_recommendations(user_id)
    print(f"Recommended artworks: {recommendations}")
    return recommendations

if __name__ == "__main__":
    example_usage()