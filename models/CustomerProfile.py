from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CustomerProfile(Base):
    __tablename__ = "customer_profiles"
    __table_args__ = (
        UniqueConstraint("email", name="uq_customer_email"),
        UniqueConstraint("phone", name="uq_customer_phone"),
        UniqueConstraint("user_id", name="uq_customer_userid"),
        UniqueConstraint("customer_id", name="uq_customer_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), nullable=False)
    customer_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=False)
    consent = Column(Boolean, default=False)
    user_id = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    registration_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    notes = Column(String(255), nullable=True)

    