from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.services.customer_order import CustomerOrderService

router = APIRouter(prefix="/orders", tags=["Customer Orders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_order(data: dict, db: Session = Depends(get_db)):
    CustomerOrderService(db).create(**data)
    return {"status": "created"}

@router.get("/{customer_id}")
def get_by_customer(customer_id: str, db: Session = Depends(get_db)):
    return CustomerOrderService(db).get_by_customer(customer_id)

@router.get("/id/{order_id}")
def get_by_order_id(order_id: str, db: Session = Depends(get_db)):
    return CustomerOrderService(db).get_by_order_id(order_id)

