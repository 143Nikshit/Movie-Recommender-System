import pickle
import streamlit as st
import requests

# Function to fetch the movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# Function to recommend movies
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:11]:  # Change to display top 10 recommendations
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error in generating recommendations: {e}")
        return [], []

# Load data
st.title("🎬 Movie Recommender System")
st.markdown("Discover movies you'll love based on your favorites!")

try:
    movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except FileNotFoundError as e:
    st.error("Required data files not found! Please ensure 'movie_list.pkl' and 'similarity.pkl' are in the correct location.")
    st.stop()

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🎥 Select or search for a movie from the dropdown:",
    movie_list
)

# Recommendation button and display
if st.button('🔍 Show Recommendations'):
    st.markdown(f"### Recommendations based on **{selected_movie}**:")
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display recommendations in a grid
    if recommended_movie_names:
        # Display 2 rows of 5 movies each
        rows = 2
        movies_per_row = 5
        for row in range(rows):
            cols = st.columns(movies_per_row)
            for idx, col in enumerate(cols):
                movie_index = row * movies_per_row + idx
                if movie_index < len(recommended_movie_names):
                    with col:
                        st.image(recommended_movie_posters[movie_index], width=150)
                        st.markdown(f"**{recommended_movie_names[movie_index]}**")
    else:
        st.warning("No recommendations available. Please try a different movie.")

# Footer
st.markdown("---")
