from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.services.stock_price import StockPriceService

router = APIRouter(prefix="/stock-prices", tags=["Stock Prices"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_price(stock_name: str, exchange_name: str, price: float, db: Session = Depends(get_db)):
    StockPriceService(db).create(stock_name, exchange_name, price)
    return {"status": "created"}

@router.get("/")
def get_latest(stock_name: str, exchange_name: str, db: Session = Depends(get_db)):
    result = StockPriceService(db).get_latest(stock_name, exchange_name)
    return result

