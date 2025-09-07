from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import CustomerProfile
from datetime import datetime

class CustomerProfileService:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        from models import CustomerProfile
        customer = CustomerProfile(**kwargs)
        self.session.add(customer)
        self.session.commit()

    def get_by(self, field, value):
        from models import CustomerProfile
        if field not in ["customer_id", "email", "phone", "user_id"]:
            raise ValueError("Invalid field")
        return self.session.query(CustomerProfile).filter(
            getattr(CustomerProfile, field) == value,
            CustomerProfile.deleted == False
        ).order_by(CustomerProfile.created_at.desc()).first()

    def update_status(self, customer_id, active):
        customer = self.get_by("customer_id", customer_id)
        if customer:
            customer.active = active
            self.session.commit()

    def delete(self, customer_id):
        customer = self.get_by("customer_id", customer_id)
        if customer:
            customer.deleted = True
            self.session.commit()
    


# Example usage of the service

# from session import SessionLocal
# from services import (
#     StockPriceService,
#     CustomerProfileService,
#     JobberJobService,
#     CustomerOrderService,
#     CustomerPositionService,
#     CustomerAlgoSubscriptionService
# )

# session = SessionLocal()

# profile_service = CustomerProfileService(session)
# profile_service.create(
#     customer_id="CUST001",
#     customer_name="John Doe",
#     phone="9876543210",
#     email="john@example.com",
#     consent=True,
#     user_id="john_doe",
#     password_hash="hashed_pw",
#     registration_date=datetime.utcnow().date()
# )
