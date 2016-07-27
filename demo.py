from random import randint

from models import Jobs, JobOjbs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sys import argv
from os import path

from sys_setup import files, required

engine = create_engine('sqlite:///data.db')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

time = datetime.utcnow()
year = time.year
month = time.month

user = ['Tim', 'Alan', 'John', 'Me']
titles = ['Car park', 'Tea pot', 'Fish Cakes', 'School']

for i in range(1, int(argv[1])):
    job = Jobs(number=i,
               year=year,
               month=randint(1, 12),
               desc=titles[randint(0, len(titles)-1)])
    job.create_job()
    folders = job.find_objects()
    session.add_all(folders)
    session.add(job)

    for f in files:
        obj = JobOjbs(object_path=path.join(job.root_path, f),
                      job_number=job.number,
                      job_year=job.year)
        obj.copy_file(required)
        obj.setup()
        session.add(obj)

session.commit()
