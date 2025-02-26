import os
import pandas as pd
import requests
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

class DataPipelineService:
    def __init__(self):
        # Database connection settings
        self.db_url = os.getenv('DATABASE_URL', 'sqlite:///data.db')  # Default to SQLite for simplicity
        self.engine = create_engine(self.db_url)

    def extract_from_api(self, api_url):
        """Extract data from a REST API."""
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()
            logging.info(f"Data extracted from API: {api_url}")
            return pd.DataFrame(data)
        except requests.RequestException as e:
            logging.error(f"Error extracting data from API: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error

    def extract_from_database(self, query):
        """Extract data from a database."""
        try:
            with self.engine.connect() as connection:
                data = pd.read_sql(query, connection)
                logging.info("Data extracted from database.")
                return data
        except SQLAlchemyError as e:
            logging.error(f"Error extracting data from database: {e}")
            return pd.DataFrame()  # Return empty DataFrame on error

    def transform_data(self, df):
        """Transform the data as needed."""
        # Example transformation: drop duplicates and fill missing values
        df = df.drop_duplicates()
        df.fillna(method='ffill', inplace=True)  # Forward fill for missing values
        logging.info("Data transformed.")
        return df

    def load_to_database(self, df, table_name):
        """Load data into a database table."""
        try:
            with self.engine.connect() as connection:
                df.to_sql(table_name, con=connection, if_exists='replace', index=False)
                logging.info(f"Data loaded into table: {table_name}")
        except SQLAlchemyError as e:
            logging.error(f"Error loading data into database: {e}")

    def run_pipeline(self, api_url, query, table_name):
        """Run the ETL pipeline."""
        # Extract
        api_data = self.extract_from_api(api_url)
        db_data = self.extract_from_database(query)

        # Combine data (if needed)
        combined_data = pd.concat([api_data, db_data], ignore_index=True)

        # Transform
        transformed_data = self.transform_data(combined_data)

        # Load
        self.load_to_database(transformed_data, table_name)

if __name__ == "__main__":
    # Example usage
    pipeline_service = DataPipelineService()
    
    # Define API URL and SQL query
    api_url = os.getenv('API_URL', 'https://api.example.com/data')
    sql_query = "SELECT * FROM existing_table"
    target_table = "combined_data"

    # Run the ETL pipeline
    pipeline_service.run_pipeline(api_url, sql_query, target_table)
