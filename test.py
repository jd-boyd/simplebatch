import json
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData


from pbatch.model import PendingJob, init


engine = create_engine('sqlite:///jobs.db', echo=True)
metadata = MetaData()
metadata.bind = engine
Session = sessionmaker(bind=engine)

init(engine)

session = Session()
q = session.query(PendingJob)
print q

pj = PendingJob("bob", "Bob Fullname", "")
pj.env = json.dumps(dict(os.environ))

session.add(pj)
session.commit()
