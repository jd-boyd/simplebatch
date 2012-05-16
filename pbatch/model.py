import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import ForeignKey, ColumnDefault

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)
    uid = Column(Integer)
    gid = Column(Integer)
    user = Column(String)
    command = Column(String)
    args = Column(String)
    env = Column(String)
    stdin = Column(String)
    stdout = Column(String)
    stderr = Column(String)

    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'jobs',
        'polymorphic_on':type
    }
      
    #def __repr__(self):
    #    #return "<Job('%s','%s', '%s')>" % (self.name, self.fullname, self.password)
    #    return "<Job()>"

class PendingJob(Job):
    __tablename__ = 'pending_jobs';
    __table_args__ = {'sqlite_autoincrement': True}
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

def connect(db_str = 'sqlite:///jobs.db'):
    import sys
    sys.stderr.write("Connect: %s\n" % db_str)
    engine = create_engine(db_str, echo=True)
    metadata = MetaData()
    metadata.bind = engine
    Session = sessionmaker(bind=engine)
    
    init(engine)

    session = Session()
    return session
