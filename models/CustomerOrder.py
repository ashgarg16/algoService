from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class CustomerOrder(Base):
    __tablename__ = "customer_orders"
    __table_args__ = (UniqueConstraint("order_id", name="uq_order_id"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    order_id = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    stock_name = Column(String(50), nullable=False)
    exchange_name = Column(String(50), nullable=False)
    order_type = Column(String(10), nullable=False)  # BUY or SELL
    execution_type = Column(String(10), nullable=False)  # MARKET or LIMIT
    position_type = Column(String(15), nullable=False)  # INTRADAY or POSITIONAL
    order_status = Column(String(15), nullable=False)  # PENDING, COMPLETED, REJECTED
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    notes = Column(String(255), nullable=True)

    