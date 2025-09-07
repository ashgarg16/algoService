from sqlalchemy.orm import Session
from models import CustomerPosition
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class CustomerPositionService:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        from models import CustomerPosition
        position = CustomerPosition(**kwargs)
        self.session.add(position)
        self.session.commit()

    def get_by_customer(self, customer_id):
        from models import CustomerPosition
        return self.session.query(CustomerPosition).filter_by(customer_id=customer_id).all()

    def get_by_customer_and_stock(self, customer_id, stock_name):
        from models import CustomerPosition
        return self.session.query(CustomerPosition).filter_by(customer_id=customer_id, stock_name=stock_name).all()
