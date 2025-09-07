from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class StockPrice(Base):
    __tablename__ = "stock_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    stock_name = Column(String(50), nullable=False)
    exchange_name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

    
