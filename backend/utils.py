import csv


def format_recommendations(recommendations):
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
    recommendations_data = recommendations
    
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
