from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import DB_CONFIG  # Your DB credentials

# Build the PostgreSQL connection string
DATABASE_URL = (
    f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


#  Purpose of session.py
# - Creates the SQLAlchemy engine using your database credentials
# - Initializes a session factory (SessionLocal) that can be injected into routes and services
# - Ensures that each request gets a clean, isolated database session

