from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
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
def create_order(
    order_id: str,
    customer_id: str,
    stock_name: str,
    exchange_name: str,
    order_type: str,
    execution_type: str,
    position_type: str,
    order_status: str,
    price: float,
    quantity: int,
    lot_count: int = 1,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    CustomerOrderService(db).create(
        order_id=order_id,
        customer_id=customer_id,
        stock_name=stock_name,
        exchange_name=exchange_name,
        order_type=order_type,
        execution_type=execution_type,
        position_type=position_type,
        order_status=order_status,
        price=price,
        quantity=quantity,
        lot_count=lot_count,
        notes=notes
    )
    return {"status": "created"}

@router.get("/{customer_id}")
def get_by_customer(customer_id: str, db: Session = Depends(get_db)):
    return CustomerOrderService(db).get_by_customer(customer_id)

@router.get("/id/{order_id}")
def get_by_order_id(order_id: str, db: Session = Depends(get_db)):
    return CustomerOrderService(db).get_by_order_id(order_id)