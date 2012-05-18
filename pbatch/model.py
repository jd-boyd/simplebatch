import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy import ForeignKey, ColumnDefault

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(Integer, primary_key=True)

    status = Column(Enum("pending", "running", "complete"))

    uid = Column(Integer)
    gid = Column(Integer)
    user = Column(String)
    command = Column(String)
    args = Column(String)
    env = Column(String)
    stdin = Column(String)
    stdout = Column(String)
    stderr = Column(String)

    start_time = Column(DateTime) # set when running

    end_time = Column(DateTime) # set when complete
    return_code = Column(Integer) # set when complete


    type = Column(String)

    __mapper_args__ = {
        'polymorphic_identity':'jobs',
        'polymorphic_on':type
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
