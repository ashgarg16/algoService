
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean,
    UniqueConstraint, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class JobberJob(Base):
    __tablename__ = "jobber_jobs"
    __table_args__ = (UniqueConstraint("jobber_id", name="uq_jobber_id"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    jobber_id = Column(String(50), nullable=False)
    customer_id = Column(String(50), nullable=False)
    security = Column(String(50), nullable=False)
    start_price = Column(Float, nullable=False)
    step_size_buy = Column(Float, nullable=False)
    direction = Column(String(10), nullable=False)  # LONG or SHORT
    step_size_sell = Column(Float, nullable=False)
    lot_multiplier = Column(String(10), nullable=False)  # FLAT, LINEAR, BINARY
    no_of_steps = Column(Integer, nullable=False)
    re_enter = Column(Boolean, default=False)
    end_date = Column(Date, nullable=False)
    auto_rollover = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    deleted = Column(Boolean, default=False)
    notes = Column(String(255), nullable=True)
