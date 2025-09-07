from sqlalchemy.orm import Session
from models import CustomerAlgoSubscription
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class CustomerAlgoSubscriptionService:
    def __init__(self, session):
        self.session = session

    def subscribe(self, **kwargs):
        from models import CustomerAlgoSubscription
        sub = CustomerAlgoSubscription(**kwargs)
        self.session.add(sub)
        self.session.commit()

    def cancel(self, customer_id, algo_name, subscription_date, notes="Cancelled"):
        self.subscribe(
            customer_id=customer_id,
            algo_name=algo_name,
            subscription_date=subscription_date,
            status="CANCELLED",
            notes=notes
        )

    def get_by_customer(self, customer_id):
        from models import CustomerAlgoSubscription
        return self.session.query(CustomerAlgoSubscription).filter_by(customer_id=customer_id).all()

    def get_active(self, customer_id):
        from models import CustomerAlgoSubscription
        return self.session.query(CustomerAlgoSubscription).filter_by(customer_id=customer_id, status="ACTIVE").all()

    