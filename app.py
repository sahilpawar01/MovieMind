# Importing libraries
import os
import pickle
import streamlit as st
import requests


# Fetching movie poster from the api
TMDB_API_KEY = os.getenv("TMDB_API_KEY", st.secrets.get("TMDB_API_KEY", ""))
TMDB_BEARER = os.getenv("TMDB_BEARER_TOKEN", st.secrets.get("TMDB_BEARER_TOKEN", ""))


def fetch_poster(movie_id):
    if not TMDB_API_KEY or not TMDB_BEARER:
        return ""

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "Authorization": f"Bearer {TMDB_BEARER}",
        "accept": "application/json"
    }
    params = {
        "api_key": TMDB_API_KEY
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        return ""

    data = response.json()
    poster_path = data.get("poster_path")
    if not poster_path:
        return ""
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Getting the recommended movies names and posters
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Web application design
st.header('Movies Recommended System')

if not TMDB_API_KEY or not TMDB_BEARER:
    st.warning(
        "TMDB credentials are missing. Set `TMDB_API_KEY` and "
        "`TMDB_BEARER_TOKEN` as environment variables or in `.streamlit/secrets.toml`."
    )

with open('movie_list.pkl', 'rb') as movie_file:
    movies = pickle.load(movie_file)

with open('similarity.pkl', 'rb') as similarity_file:
    similarity = pickle.load(similarity_file)

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Select a movie from dropdown",
    movie_list
)


# Displaying the recommended movie names and posters
if st.button('Show Recommended Movies'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
