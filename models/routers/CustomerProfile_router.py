from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.services.customer_profile import CustomerProfileService
from app.models import CustomerProfile
from datetime import date

router = APIRouter(prefix="/customers", tags=["Customer Profiles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_customer(profile: CustomerProfile, db: Session = Depends(get_db)):
    service = CustomerProfileService(db)
    service.create(**profile.dict())
    return {"status": "created"}

@router.get("/{customer_id}")
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    service = CustomerProfileService(db)
    customer = service.get_by("customer_id", customer_id)
    return customer

@router.put("/{customer_id}/status")
def update_status(customer_id: str, active: bool, db: Session = Depends(get_db)):
    service = CustomerProfileService(db)
    service.update_status(customer_id, active)
    return {"status": "updated"}

@router.delete("/{customer_id}")
def delete_customer(customer_id: str, db: Session = Depends(get_db)):
    service = CustomerProfileService(db)
    service.delete(customer_id)
    return {"status": "deleted"}

#  To run
# uvicorn app.main:app --reload
# Your API will be live at http://localhost:8000, with automatic Swagger docs at /docs.

