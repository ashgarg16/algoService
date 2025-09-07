from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.services.algo_subscription import CustomerAlgoSubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["Algo Subscriptions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def subscribe(data: dict, db: Session = Depends(get_db)):
    CustomerAlgoSubscriptionService(db).subscribe(**data)
    return {"status": "subscribed"}

@router.post("/cancel")
def cancel(customer_id: str, algo_name: str, subscription_date: str, db: Session = Depends(get_db)):
    CustomerAlgoSubscriptionService(db).cancel(customer_id, algo_name, subscription_date)
    return {"status": "cancelled"}

@router.get("/{customer_id}")
def get_all(customer_id: str, db: Session = Depends(get_db)):
    return CustomerAlgoSubscriptionService(db).get_by_customer(customer_id)

@router.get("/{customer_id}/active")
def get_active(customer_id: str, db: Session = Depends(get_db)):
    return CustomerAlgoSubscriptionService(db).get_active(customer_id)
