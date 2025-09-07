from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CustomerPosition(Base):
    __tablename__ = "customer_positions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    customer_id = Column(String(50), nullable=False)
    stock_name = Column(String(50), nullable=False)
    exchange_name = Column(String(50), nullable=False)
    position_type = Column(String(10), nullable=False)  # BUY or SELL
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    notes = Column(String(255), nullable=True)

    