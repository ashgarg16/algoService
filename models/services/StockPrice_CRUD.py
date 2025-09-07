from sqlalchemy.orm import Session
from models import StockPrice
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class StockPriceService:
    def __init__(self, session):
        self.session = session

    def create(self, stock_name, exchange_name, price):
        from models import StockPrice
        entry = StockPrice(stock_name=stock_name, exchange_name=exchange_name, price=price)
        self.session.add(entry)
        self.session.commit()

    def get_latest(self, stock_name, exchange_name):
        from models import StockPrice
        return self.session.query(StockPrice).filter_by(
            stock_name=stock_name,
            exchange_name=exchange_name
        ).order_by(StockPrice.timestamp.desc()).first()
    
    