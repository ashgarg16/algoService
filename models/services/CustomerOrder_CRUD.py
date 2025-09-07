from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List
from app.models import CustomerOrder

class CustomerOrderService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **kwargs) -> bool:
        try:
            order = CustomerOrder(timestamp=datetime.utcnow(), **kwargs)
            self.session.add(order)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Order insert failed: {e}")
            return False

    def get_by_customer(self, customer_id: str) -> List[CustomerOrder]:
        return self.session.query(CustomerOrder).filter_by(customer_id=customer_id).order_by(CustomerOrder.timestamp.desc()).all()

    def get_by_order_id(self, order_id: str) -> CustomerOrder | None:
        return self.session.query(CustomerOrder).filter_by(order_id=order_id).first()
    
    