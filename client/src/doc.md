# TindeArt Recommendation System Documentation

## How It Works

TindeArt uses a sophisticated recommendation system that learns your art preferences through your interactions (swipes) and provides personalized art recommendations. Here's how it works:

### 1. Image Analysis
When an artwork is added to our system, we analyze it using three main feature categories:

#### Color Features
- Extracts 5 dominant colors from the artwork
- Calculates the proportion of each dominant color
- Measures color distribution (mean and standard deviation) across RGB channels

#### Color Distribution (Histogram)
- Creates detailed color histograms with 8 bins for each RGB channel
- Captures how colors are distributed throughout the artwork
- Helps identify artworks with similar color patterns

#### Composition Features
- Analyzes the artwork's composition by dividing it into a 3x3 grid
- Measures brightness levels in each section
- Calculates overall brightness and contrast

### 2. Learning Your Preferences

The system learns your preferences in two ways:

#### For New Users (Cold Start)
- Initially uses a similarity-based approach
- Recommends artworks with features similar to ones you've liked
- Uses cosine similarity to find artworks with matching characteristics

#### For Established Users
- After you've liked/disliked at least 5 artworks each
- Switches to a machine learning model (Random Forest Classifier)
- Creates a personalized preference profile based on your swipe history
- Predicts whether you'll like new artworks based on their features

### 3. Continuous Learning

The system continuously improves as you interact with more artworks:
- Updates your preference profile with each swipe
- Refines recommendations based on your latest interactions
- Adapts to changes in your taste over time

### 4. Dataset

The recommendations come from a curated collection of artworks from WikiArt, including various:
- Artistic styles
- Genres
- Time periods
- Artists

## Privacy Note

The system only stores anonymous user IDs and artwork interaction data. No personal information is required or stored.