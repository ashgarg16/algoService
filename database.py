from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# For dev: SQLite file DB
# For prod: "postgresql+psycopg2://user:pass@host/dbname"
DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ------------------ DB Dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()