from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.session import SessionLocal
from app.services.jobber_job import JobberJobService

router = APIRouter(prefix="/jobs", tags=["Jobber Jobs"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_job(data: dict, db: Session = Depends(get_db)):
    JobberJobService(db).create(**data)
    return {"status": "created"}

@router.get("/{jobber_id}")
def get_job(jobber_id: str, db: Session = Depends(get_db)):
    return JobberJobService(db).get_by_id(jobber_id)

@router.delete("/{jobber_id}")
def delete_job(jobber_id: str, db: Session = Depends(get_db)):
    JobberJobService(db).delete(jobber_id)
    return {"status": "deleted"}

@router.put("/{jobber_id}/toggle")
def toggle_active(jobber_id: str, active: bool, db: Session = Depends(get_db)):
    JobberJobService(db).toggle_active(jobber_id, active)
    return {"status": "updated"}