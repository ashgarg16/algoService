from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List
from app.models import CustomerPosition

class CustomerPositionService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **kwargs) -> bool:
        try:
            position = CustomerPosition(timestamp=datetime.utcnow(), **kwargs)
            self.session.add(position)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Position insert failed: {e}")
            return False

    def get_by_customer(self, customer_id: str) -> List[CustomerPosition]:
        return self.session.query(CustomerPosition).filter_by(customer_id=customer_id).order_by(CustomerPosition.timestamp.desc()).all()

    def get_by_customer_and_stock(self, customer_id: str, stock_name: str) -> List[CustomerPosition]:
        return self.session.query(CustomerPosition).filter_by(customer_id=customer_id, stock_name=stock_name).order_by(CustomerPosition.timestamp.desc()).all()

    def update_position_status(self, position_id: int, status: str) -> bool:
        try:
            position = self.session.query(CustomerPosition).filter_by(id=position_id).first()
            if not position:
                return False
            position.position_status = status
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Status update failed: {e}")
            return False
