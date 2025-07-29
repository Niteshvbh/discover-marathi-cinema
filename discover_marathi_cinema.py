# -*- coding: utf-8 -*-
"""
Created on Wed Jul 16 14:34:05 2025

@author: Nitesh
"""
import pandas as pd
import streamlit as st
import requests

# Load dataset
url = "https://storage.googleapis.com/marathi-cinema-assests/Posters/Movie_Dataset.csv"
df = pd.read_csv(url)

# Setup UI
st.title("Discover Marathi Cinema")
st.sidebar.header("🎬 Filter Your Preferences")

# Genre and Vibe selectors
selected_genres = st.sidebar.multiselect(
    "Select Genres", 
    ["Drama", "Romance", "Comedy", "Thriller", "Social", "Family"], 
    default=["Drama"]
)

selected_vibe = st.sidebar.selectbox(
    "Select a Vibe", 
    ["emotional", "realistic", "entertaining", "thought-provoking", "grand"],
    index=0
)

# Define reusable display functiondef display_movies(movies_df):
# Define reusable display function
def display_movies(movies_df):
    num_columns = 4
    num_movies = len(movies_df)

    for i in range(0, num_movies, num_columns):
        row = st.columns(num_columns)
        for j in range(num_columns):
            if i + j < num_movies:
                movie = movies_df.iloc[i + j]
                with row[j]:
                    # ✅ Check if poster_url exists and is valid
                    poster = movie.get('poster_url', '')

                    # Ensure poster is a string (convert from NaN) and strip whitespace
                    poster = str(movie.get('poster_url', '')).strip()

                    try:
                        if poster.startswith("http"):
                            if not poster or not poster.startswith("http"):
                                st.markdown("🚫 *Poster not available*")
                                st.caption(f"(Missing or invalid URL: {poster})")
                            st.caption(f"Poster URL: {poster}")
                            st.image(poster, use_container_width=True)
                        else:
                            st.markdown("🚫 *Poster not available*")
                    except Exception as e:
                        st.warning("⚠️ Could not load image.")
                        st.text(f"Error: {e}")


                    # Title and genre
                    st.markdown(
                        f"<div style='text-align: center; font-weight: bold; margin-top: 8px;'>{movie['title']}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div style='text-align: center; font-style: italic;'>Genre: {movie['genre']}</div>",
                        unsafe_allow_html=True
                    )

st.markdown(f"""
> *"Ready for a {selected_vibe} ride through Marathi cinema? 🎥 Let's go!"*
> - **Sharvari**
""")

# Create Tabs
if selected_genres:
    tab1, tab2 = st.tabs(["🔍 Filtered Suggestions", "🤖 AI Recommendations"])

    with tab1:
        filtered_movies = df[df['genre'].str.contains('|'.join(selected_genres), case=False, na=False)]

        st.markdown("### 🎬 Recommended Movies for Genres: " + ', '.join(selected_genres))

        # 👇 call display_movies only after filtered_movies is defined
        display_movies(filtered_movies)


    with tab2:
        if "ai_movies" not in st.session_state:
            st.session_state.ai_movies = None

        if st.sidebar.button("Get Recommendations"):
            with st.spinner("Fetching AI recommendations..."):
                response = requests.post(
                    "https://us-central1-turnkey-axiom-463314-v3.cloudfunctions.net/recommend_movies",
                    json={"genres": selected_genres, "vibe": selected_vibe}
                )
                if response.status_code == 200:
                    movies = response.json()
                    ai_movies_df = pd.DataFrame(movies)

                    if 'poster_url' not in ai_movies_df.columns:
                        ai_movies_df['poster_url'] = ""

                    st.session_state.ai_movies = ai_movies_df
                else:
                    st.error("Failed to fetch recommendations. Try again.")

        if st.session_state.ai_movies is not None:
            st.markdown("### 🤖 AI-Based Recommendations")
            display_movies(st.session_state.ai_movies)


# Optional pandas display settings
pd.set_option("display.max_columns", 5)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", 200)

# Fun footer
st.markdown("""
---
*“Whenever I get sad, I stop being sad and start recommending Marathi movies. True story.”*  
— **Sharvari**, the AI  
Built with ❤️ using Streamlit | By Nitesh
""")


