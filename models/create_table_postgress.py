# create_tables.py

from sqlalchemy import create_engine
from models import Base
from config import DB_CONFIG

# Build the PostgreSQL connection string
DATABASE_URL = (
    f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

# Create engine and bind metadata
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

print("✅ All tables created successfully.")


# runnning
# python create_tables.py

