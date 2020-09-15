from sqlalchemy import Column, Integer, Text, DateTime
from models.database import Base
from datetime import datetime


class AllJobs(Base):
    __tablename__ = "alljobs"
    id = Column(Integer, primary_key=True)
    job_id = Column(Text, unique=True)
    sampler = Column(Text)
    date = Column(DateTime, default=datetime.now())
    state = Column(Text)

    def __init__(self, job_id=None, sampler=None, state=None, date=None):
        self.job_id = job_id
        self.sampler = sampler
        self.state = "Waiting"
        self.date = date

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "sampler": self.sampler,
            "state": self.state,
            "date": self.date,
        }
