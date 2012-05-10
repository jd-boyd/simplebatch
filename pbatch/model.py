import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, ColumnDefault

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    gid = Column(Integer)
    user = Column(String)
    cli = Column(String)
    env = Column(String)
    stdin = Column(String)
    stdout = Column(String)
    stderr = Column(String)

    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'jobs',
        'polymorphic_on':type
    }

    def __init__(self, name, fullname, password):
        #self.name = name
        #self.fullname = fullname
        #self.password = password
        pass
        
    #def __repr__(self):
    #    #return "<Job('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
    #    return "<Job()>"


class PendingJob(Job):
    __tablename__ = 'pending_jobs';
    
    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'pending_jobs',
    }


class RunningJob(Job):
    __tablename__ = 'running_jobs';
    start_time = Column(DateTime)
   
    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity':'running_jobs',
    }


class CompletedJob(Job):
    __tablename__ = 'completed_jobs';
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    return_code = Column(Integer)

    job_id = Column(Integer, ForeignKey('jobs.job_id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity':'completed_jobs',
    }

def init(engine):
    Base.metadata.create_all(engine)

