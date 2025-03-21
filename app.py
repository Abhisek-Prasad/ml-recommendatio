import os
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:3DUs8n3*]x#cz?J(?<mJh!?SakNr@uat-backend-database.cf482umqeit1.ap-south-1.rds.amazonaws.com:5432/sakshemit'

def get_database_connection():
    """Create and return database engine"""
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        return engine
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None

def print_database_tables():
    """Print all tables in the database"""
    engine = get_database_connection()
    if engine:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print("\nDatabase Tables:")
        for table in tables:
            print(f"- {table}")
            # Print columns for each table
            columns = inspector.get_columns(table)
            print("  Columns:")
            for column in columns:
                print(f"    - {column['name']}: {column['type']}")

def test_db_connection():
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        with engine.connect() as connection:
            result = connection.execute("SELECT version();")
            print("Connected to database. Version:", result.fetchone()[0])
    except Exception as e:
        print("Error connecting to database:", str(e))

if __name__ == "__main__":
    test_db_connection()
