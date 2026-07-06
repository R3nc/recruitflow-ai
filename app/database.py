# Import SQLModel components:
#   SQLModel - base class for models and metadata container
#   create_engine - creates the database engine connection
#   Session - lets us interact with the database
from sqlmodel import SQLModel, create_engine, Session


# The database file path. SQLite creates this file automatically
# if it does not exist when the engine first connects.
# "sqlite:///recruitflow.db" means a local file named recruitflow.db
DATABASE_URL = "sqlite:///recruitflow.db"

# Create the engine — the starting point for any SQLAlchemy/SQLModel
# application. The engine manages the database connection pool.
# "check_same_thread=False" is required for SQLite so we can share
# the connection across multiple threads (e.g. when FastAPI handles
# multiple requests concurrently).
# "echo=True" prints every SQL query to the console (helpful for debugging).
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,
)


def create_db_and_tables():
    """
    Create all database tables defined by SQLModel models.

    This reads every class that inherits from SQLModel with table=True
    and runs CREATE TABLE statements in the database.
    Call this once when the application starts.
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Generator function that provides a database session.

    Each call yields a Session object wrapped in a 'with' block so it
    is automatically closed (and the connection returned to the pool)
    when the caller is done. FastAPI's Depends can use this directly.
    """
    with Session(engine) as session:
        yield session
