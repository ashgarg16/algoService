from sqlalchemy.orm import Session
from models import CustomerOrder
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class CustomerOrderService:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        from models import CustomerOrder
        order = CustomerOrder(**kwargs)
        self.session.add(order)
        self.session.commit()

    def get_by_customer(self, customer_id):
        from models import CustomerOrder
        return self.session.query(CustomerOrder).filter_by(customer_id=customer_id).all()

    def get_by_order_id(self, order_id):
        from models import CustomerOrder
        return self.session.query(CustomerOrder).filter_by(order_id=order_id).first()
