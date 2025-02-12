import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your anime dataset
anime_df = pd.read_csv('anime.csv')  # Assuming it has 'title' and 'genre' columns

# Fill missing genres
anime_df['genre'] = anime_df['genre'].fillna('')

# Vectorize genres
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(anime_df['genre'])

# Compute cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend anime
def recommend_anime(title, cosine_sim=cosine_sim):
    idx = anime_df[anime_df['name'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]  # Get top 5 similar anime
    
    anime_indices = [i[0] for i in sim_scores]
    return anime_df['name'].iloc[anime_indices]

# Example usage
recommendations = recommend_anime('Hunter x Hunter (2011)')
print(recommendations)
