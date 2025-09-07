from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.services.client_broker import ClientBrokerService

router = APIRouter(prefix="/client-broker", tags=["Client Broker"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_broker_record(data: dict, db: Session = Depends(get_db)):
    ClientBrokerService(db).create(**data)
    return {"status": "created"}

@router.get("/")
def query_broker_records(
    customer_id: str = None,
    broker_name: str = None,
    account_id: str = None,
    db: Session = Depends(get_db)
):
    results = ClientBrokerService(db).get_by_filters(
        customer_id=customer_id,
        broker_name=broker_name,
        account_id=account_id
    )
    return results

