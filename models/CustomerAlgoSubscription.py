from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CustomerAlgoSubscription(Base):
    __tablename__ = "customer_algo_subscriptions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(String(50), nullable=False)
    algo_name = Column(String(100), nullable=False)
    subscription_date = Column(Date, nullable=False)
    status = Column(String(15), nullable=False)  # ACTIVE, CANCELLED, EXPIRED
    notes = Column(String(255), nullable=True)

    
