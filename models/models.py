from datetime import datetime

from sqlalchemy import Text, Column, Integer, DateTime

from models.database import Base


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    job_id = Column(Text, unique=True)
    sampler = Column(Text)
    state = Column(Text)
    # matrix = Column(ARRAY(Integer, dimensions=2))
    date = Column(DateTime, default=datetime.now())

    def __init__(self, job_id=None, sampler=None, state=None, date=None):
        self.job_id = job_id
        self.sampler = sampler
        self.state = state
        # self.matrix = matrix
        self.date = date

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "sampler": self.sampler,
            "state": self.state,
            "date": self.date,
        }
