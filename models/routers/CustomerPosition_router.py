from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.services.customer_position import CustomerPositionService

router = APIRouter(prefix="/positions", tags=["Customer Positions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_position(data: dict, db: Session = Depends(get_db)):
    CustomerPositionService(db).create(**data)
    return {"status": "created"}

@router.get("/{customer_id}")
def get_by_customer(customer_id: str, db: Session = Depends(get_db)):
    return CustomerPositionService(db).get_by_customer(customer_id)

@router.get("/{customer_id}/{stock_name}")
def get_by_customer_and_stock(customer_id: str, stock_name: str, db: Session = Depends(get_db)):
    return CustomerPositionService(db).get_by_customer_and_stock(customer_id, stock_name)
