from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKeyConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

from sys_setup import system_path, create_job_folders, create_yr_dir, job_archive
from pathlib import Path as P
from os import path
import shutil
from workout import find_objects

engine = create_engine('sqlite:///data.db')
Base = declarative_base()


class JobOjbs(Base):
    __tablename__ = "job_objects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    object_type = Column(String)
    create_date = Column(DateTime)
    job_number = Column(Integer,)
    job_year = Column(Integer)
    object_path = Column(String)
    ForeignKeyConstraint(['job_number', 'job_year'], ['Jobs.number', 'Jobs.year'])
    # jobs = relationship("Jobs", back_populates="job_objects")

    def setup(self):
        ojb = P(self.object_path)
        self.name = ojb.name

        if ojb.is_dir():
            self.object_type = "Folder"
        else:
            name = ojb.name
            name = name.split(".")
            self.object_type = name[1]

        self.create_date = datetime.utcnow()

    def __repr__(self):
        return "<Document %s>" % self.name


class Jobs(Base):
    __tablename__ = "jobs"

    number = Column(Integer, primary_key=True)
    year = Column(Integer, primary_key=True)
    month = Column(Integer)
    desc = Column(String)
    owner_id = Column(Integer)
    entry_date = Column(DateTime)
    active = Column(Boolean, default=True)
    root_path = Column(String)

    # job_objects = relationship("JobObjs", back_populates="jobs")

    def archive(self):
        self.active = False

    def full_job_no(self):
        if self.month < 10:
            temp_month = "0" + str(self.month)
        else:
            temp_month = str(self.month)
        temp_year = str(self.year)

        temp_full_number = temp_year[2:] + '-' + temp_month + '-' + str(self.number)
        return temp_full_number

    def check_root(self):
        root = P(path.join(system_path, str(self.year)))
        if root.exists():
            return True
        else:
            create_yr_dir()
            if root.exists():
                return True
            else:
                raise RuntimeError

    def create_job(self):
        if self.check_root():
            self.root_path = path.join(system_path, str(self.year), self.full_job_no())
            job = P(self.root_path)
            job.mkdir()
            create_job_folders(job)
        else:
            raise RuntimeError

    def zip(self):
        backup_root = P(path.join(job_archive, str(self.year), self.full_job_no()))
        if not backup_root.exists():
            backup_root.mkdir()
        base = path.join(str(backup_root), self.full_job_no() + " " + datetime.utcnow().strftime('%Y%m%d %H%M%S'))
        shutil.make_archive(base, 'zip', root_dir=self.root_path)

    def find_objects(self):
        links = find_objects(self.root_path)
        finds = []
        for link in links:
            oh = JobOjbs(job_number=self.number, job_year=self.year, object_path=link)
            oh.setup()
            finds.append(oh)
            print(oh)
        return finds

    def __repr__(self):
        return "<Job: %s>" % (self.full_job_no())

if __name__ == '__main__':
    Base.metadata.create_all(engine)
