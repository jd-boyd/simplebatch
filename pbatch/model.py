import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///jobs.db:', echo=True)

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    gid = Column(Integer)
    user = Column(String)
    user = Column(String)
    cli = Column(String)
    env = Column(String)
    stdin = Column(String)
    stdout = Column(String)
    stderr = Column(String)

    def __init__(self, name, fullname, password):
        #self.name = name
        #self.fullname = fullname
        #self.password = password
        pass
        
    def __repr__(self):
        #return "<Job('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
        return "<Job()>"


class Pending(Job):
    __tablename__ = 'pending_jobs';
    pass

class Running(Job):
    __tablename__ = 'running_jobs';
    #starting_time
    pass

class Complete(Job):
    __tablename__ = 'completed_jobs';
    #starting_time
    #ending time
    return_code = Column(Integer)
