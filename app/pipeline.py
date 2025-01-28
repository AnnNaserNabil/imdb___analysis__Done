import pandas as pd
import requests
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    "dbname": os.getenv("PGDATABASE"),
    "user": os.getenv("PGUSER"),
    "password": os.getenv("PGPASSWORD"),
    "host": os.getenv("PGHOST"),
    "port": os.getenv("PGPORT", 5432)  # Use 5432 as fallback if port is missing
}

# TMDb API key (replace 'YOUR_TMDB_API_KEY' with your actual API key)
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_movie_details_tmdb(movie_id):
    """Fetch detailed information for a specific movie using TMDb API"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=credits"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching details for movie ID {movie_id}: {response.status_code}")
        return None

def fetch_movies_by_year_tmdb(year, top_n=20):
    """Fetch top movies for a specific year using TMDb API"""
    url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&primary_release_year={year}&sort_by=vote_average.desc"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        movies = data.get("results", [])[:top_n]
        detailed_movies = []
        for movie in movies:
            details = fetch_movie_details_tmdb(movie.get("id"))
            if details:
                detailed_movies.append(details)
        return detailed_movies
    else:
        print(f"Error fetching data for year {year}: {response.status_code}")
        return []

def extract_data_tmdb():
    """Extract top-rated movies from TMDb API"""
    years = range(2000, 2021)  # Adjust the year range as needed
    all_movies = []
    
    for year in years:
        print(f"Fetching data for year {year}...")
        movies = fetch_movies_by_year_tmdb(year)
        for movie in movies:
            title = movie.get("title")
            year = year
            rating = float(movie.get("vote_average", 0))
            movie_id = movie.get("id")
            genres = ", ".join([genre["name"] for genre in movie.get("genres", [])])
            directors = ", ".join([crew["name"] for crew in movie.get("credits", {}).get("crew", []) if crew["job"] == "Director"])
            actors = ", ".join([cast["name"] for cast in movie.get("credits", {}).get("cast", [])[:5]])  # Top 5 actors
            all_movies.append({"title": title, "year": year, "rating": rating, "movie_id": movie_id, "genres": genres, "director": directors, "cast": actors})
    
    return pd.DataFrame(all_movies)

def update_database():
    """Full ETL pipeline"""
    engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

    # Extract and transform
    df = extract_data_tmdb()
    if df.empty:
        print("No data extracted. Skipping database update.")
        return

    df["decade"] = (df["year"] // 10) * 10

    # Load to database
    try:
        df.to_sql("movies", engine, if_exists="replace", index=False)
        print("Database updated successfully!")
    except Exception as e:
        print(f"Error updating database: {e}")

if __name__ == "__main__":
    update_database()