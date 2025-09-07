from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
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
def create_position(
    customer_id: str,
    stock_name: str,
    exchange_name: str,
    position_type: str,
    quantity: int,
    price: float,
    position_status: Optional[str] = "Open",
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    CustomerPositionService(db).create(
        customer_id=customer_id,
        stock_name=stock_name,
        exchange_name=exchange_name,
        position_type=position_type,
        quantity=quantity,
        price=price,
        position_status=position_status,
        notes=notes
    )
    return {"status": "created"}

@router.get("/{customer_id}")
def get_by_customer(customer_id: str, db: Session = Depends(get_db)):
    return CustomerPositionService(db).get_by_customer(customer_id)

@router.get("/{customer_id}/{stock_name}")
def get_by_customer_and_stock(customer_id: str, stock_name: str, db: Session = Depends(get_db)):
    return CustomerPositionService(db).get_by_customer_and_stock(customer_id, stock_name)

@router.put("/status/{position_id}")
def update_status(position_id: int, status: str, db: Session = Depends(get_db)):
    success = CustomerPositionService(db).update_position_status(position_id, status)
    return {"status": "updated" if success else "not found"}