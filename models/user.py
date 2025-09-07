from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")  # 'admin' or 'user'
    is_active = Column(Boolean, default=True)
    reset_token = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)

    