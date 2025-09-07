from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ClientBroker(Base):
    __tablename__ = "client_broker"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String(50), nullable=False)
    broker_name = Column(String(100), nullable=False)
    account_id = Column(String(100), nullable=False)
    account_login = Column(String(100), nullable=False)
    account_password = Column(String(255), nullable=False)
    login_parameter = Column(String(100), nullable=False)
    login_parameter_value = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    