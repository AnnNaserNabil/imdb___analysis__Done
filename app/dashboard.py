import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT", 5432)  # Default PostgreSQL port
}

@st.cache_data
def load_data():
    """Load data from PostgreSQL."""
    try:
        connection_url = (
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
        )
        engine = create_engine(connection_url)
        return pd.read_sql("SELECT * FROM movies", engine)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Helper functions for new features
def search_movie(df, title):
    """Search for a movie by title."""
    return df[df['title'].str.contains(title, case=False, na=False)]

def main():
    st.set_page_config(page_title="IMDb Analytics", layout="wide")

    # Title and description
    st.title("🎬 IMDb Top Movies Analyzer")
    st.markdown("Explore trends in IMDb's top movies")

    # Load data
    df = load_data()
    if df.empty:
        st.warning("No data available. Please update the database.")
        return

    # Sidebar controls
    st.sidebar.header("Filters")
    selected_decade = st.sidebar.slider(
        "Select Decade", 
        min_value=int(df["decade"].min()),
        max_value=int(df["decade"].max()),
        step=10,
        value=(int(df["decade"].min()), int(df["decade"].max()))
    )

    selected_year = st.sidebar.selectbox(
        "Select Year", 
        options=df["year"].unique()
    )

    min_rating, max_rating = float(df["rating"].min()), float(df["rating"].max())
    if min_rating == max_rating:
        st.sidebar.warning("All movies have the same rating.")
        selected_rating_range = (min_rating, max_rating)
    else:
        selected_rating_range = st.sidebar.slider(
            "Select Rating Range", 
            min_value=min_rating,
            max_value=max_rating,
            value=(min_rating, max_rating)
        )

    # Filter data based on selections
    filtered_df = df[
        (df["decade"] >= selected_decade[0]) & 
        (df["decade"] <= selected_decade[1]) &
        (df["year"] == selected_year) &
        (df["rating"] >= selected_rating_range[0]) &
        (df["rating"] <= selected_rating_range[1])
    ]

    # Add a rank column to the filtered DataFrame
    filtered_df = filtered_df.sort_values("rating", ascending=False).reset_index(drop=True)
    filtered_df['rank'] = filtered_df.index + 1

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Movies by Decade")
        st.dataframe(filtered_df.head(10)[["rank", "title", "year", "rating", "director", "cast"]], height=400)

    with col2:
        st.subheader("Genre Distribution")
        # Ensure 'genres' column is used as per the updated pipeline
        genre_counts = filtered_df['genres'].str.split(',').explode().str.strip().value_counts().reset_index()
        genre_counts.columns = ['genre', 'count']
        
        fig = px.bar(
            genre_counts, 
            x='genre', 
            y='count', 
            title="Genre Distribution",
            labels={"genre": "Genre", "count": "Count"},
            color_discrete_sequence=["#FF4B4B"]
        )
        st.plotly_chart(fig, use_container_width=True)

    # Additional interactive features
    st.subheader("Interactive Data Table")
    selected_movie_data = st.dataframe(filtered_df)  # Use filtered_df for the interactive data table

    # Detailed Movie Information
    st.subheader("Detailed Movie Information")
    selected_movie = st.selectbox("Select a Movie", filtered_df["title"])  # Use filtered_df for the selectbox
    if selected_movie:
        movie_info = filtered_df[filtered_df["title"] == selected_movie].iloc[0]
        st.write(f"**Title:** {movie_info['title']}")
        st.write(f"**Year:** {movie_info['year']}")
        st.write(f"**Rating:** {movie_info['rating']}")
        st.write(f"**Director:** {movie_info['director']}")
        st.write(f"**Cast:** {movie_info['cast']}")
        st.write(f"**Movie ID:** {movie_info['movie_id']}")

    # Search functionality
    search_title = st.sidebar.text_input("Search for a Movie")
    if search_title:
        search_results = search_movie(df, search_title)
        st.subheader(f"Search Results for '{search_title}'")
        st.dataframe(search_results)

if __name__ == "__main__":
    main()