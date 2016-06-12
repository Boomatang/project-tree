from models import Jobs, JobOjbs
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///data.db')
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def data_input():
    clint_name = input("Clint Name: ")
    desc = input("Project name: ")
    number = input("Project Number: ")
    return clint_name, desc, number


time = datetime.utcnow()
year = time.year
month = time.month


if __name__ == '__main__':
    numbers = session.query(Jobs.number).filter(Jobs.year == year)
    numbers = numbers.all()
    temp = []
    for i in numbers:
        temp.append(i[0])
    numbers = temp

    clint, project_name, project_number = data_input()
    if int(project_number) not in numbers:
        job = Jobs(number=project_number,
                   year=year,
                   month=month,
                   desc=project_name,
                   entry_date=datetime.utcnow())
        job.create_job()
        folders = job.find_objects()
        session.add_all(folders)
        session.add(job)
        session.commit()
        print(job)
    else:
        print('Job exists rolling back')
        session.rollback()
