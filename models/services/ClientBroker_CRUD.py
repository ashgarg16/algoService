from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from datetime import datetime

from app.models import ClientBroker  # Import your SQLAlchemy model

class ClientBrokerService:
    def __init__(self, session: Session):
        self.session = session

    def create(self, **kwargs) -> bool:
        try:
            entry = ClientBroker(created_at=datetime.utcnow(), **kwargs)
            self.session.add(entry)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"ClientBroker insert failed: {e}")
            return False

    def get_by_filters(
        self,
        customer_id: Optional[str] = None,
        broker_name: Optional[str] = None,
        account_id: Optional[str] = None
    ) -> List[ClientBroker]:
        query = self.session.query(ClientBroker)
        if customer_id:
            query = query.filter(ClientBroker.customer_id == customer_id)
        if broker_name:
            query = query.filter(ClientBroker.broker_name == broker_name)
        if account_id:
            query = query.filter(ClientBroker.account_id == account_id)
        return query.order_by(ClientBroker.created_at.desc()).all()
    
    