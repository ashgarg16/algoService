from sqlalchemy.orm import Session
from models import JobberJob
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class JobberJobService:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        from models import JobberJob
        job = JobberJob(**kwargs)
        self.session.add(job)
        self.session.commit()

    def get_by_id(self, jobber_id):
        from models import JobberJob
        return self.session.query(JobberJob).filter_by(jobber_id=jobber_id, deleted=False).order_by(JobberJob.timestamp.desc()).first()

    def delete(self, jobber_id, notes="Deleted"):
        job = self.get_by_id(jobber_id)
        if job:
            self.create(**{**job.__dict__, "deleted": True, "notes": notes})

    def toggle_active(self, jobber_id, active, notes=""):
        job = self.get_by_id(jobber_id)
        if job:
            self.create(**{**job.__dict__, "active": active, "notes": notes})
