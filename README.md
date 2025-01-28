# IMDb Analysis Project

This project is dedicated to the analysis of IMDb data using Python. The goal is to extract, process, and analyze movie data to gain insights into trends, ratings, and other relevant metrics. The analysis includes data extraction, processing, and visualization of findings.

## Features

- **Data Extraction**: Collecting data from IMDb using web scraping and APIs.
- **Data Cleaning**: Processing raw data to handle missing values, duplicates, and inconsistencies.
- **Exploratory Data Analysis (EDA)**: Analyzing data to uncover patterns and trends.
- **Data Visualization**: Creating visual representations of the data using libraries like Matplotlib and Seaborn.
- **Interactive Dashboard**: Using Streamlit to build an interactive dashboard for exploring movie data.

## Technologies

- **Python**: The primary programming language used for the analysis.
- **Pandas**: For data manipulation and analysis.
- **NumPy**: For numerical operations.
- **Matplotlib**: For creating static, animated, and interactive visualizations.
- **Seaborn**: For statistical data visualization.
- **Streamlit**: For building the interactive dashboard.
- **SQLAlchemy**: For database interactions.
- **PostgreSQL**: The database used to store and query the movie data.

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/AnnNaserNabil/imdb___analysis__Done.git

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
3. Set up the environment variables by creating a .env file with your database and API key configurations:
   ```bash
   PGDATABASE=your_database_name
   PGUSER=your_database_user
   PGPASSWORD=your_database_password
   PGHOST=your_database_host
   PGPORT=your_database_port
   TMDB_API_KEY=your_tmdb_api_key

4. Run the ETL pipeline to populate the database:
   ```bash
   python app/pipeline.py

5. Launch the Streamlit dashboard:

   ```bash
   streamlit run app/dashboard.py


## Thank You
