import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import OperationalError
from app.core.config import settings  # Assuming DATABASE_URL is in settings

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create the base class for ORM models
Base = declarative_base()


class DatabaseHelper:
    def __init__(self, database_url: str):
        self.engine = None
        self.session = None
        self.database_url = database_url

    def __enter__(self):
        """Creates a database connection and session."""
        self.engine = self.get_database_engine()
        if not self.engine:
            raise Exception("Could not create database engine.")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleans up the database session and engine."""
        self.session.close()
        self.engine.dispose()

    def get_database_engine(self):
        """Creates a database engine using the DATABASE_URL."""
        try:
            # Use the provided DATABASE_URL directly
            engine = create_engine(
                self.database_url, echo=False
            )  # Disable echo in production
            return engine
        except Exception as e:
            logger.error(f"Error creating the database engine: {e}")
            return None


# Dependency to get a database session
def get_db():
    """Yields a database session."""
    # Get the DATABASE_URL from settings
    database_url = settings.DATABASE_URL
    with DatabaseHelper(database_url) as db_helper:
        db = db_helper.session
        yield db


# Test DB connection
def test_db_connection():
    """Tests the database connection and logs the result."""
    try:
        # Get the DATABASE_URL from settings
        database_url = settings.DATABASE_URL
        with DatabaseHelper(database_url) as db_helper:
            # Trying to connect to the database to verify the connection
            db_helper.engine.connect()
            logger.info("Database connection successful.")
    except OperationalError as e:
        logger.error(
            "Database connection failed. Please check your credentials and database server."
        )
        logger.error(f"Error: {e}")
        raise


# Run DB connection test on import
test_db_connection()
