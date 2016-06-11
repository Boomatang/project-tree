from os import path
from pathlib import Path as P
from datetime import datetime
from sys import argv


def setup_sys():
    system_path = ''
    out_folders = []
    with open("sys.conf", 'r') as f:
        content = f.readlines()
        f.close()

    for line in content:
        if line[0:5] == "path=":
            system_path = line[5:-1]
        elif line[0:8] == "folders=":
            folders_temp = line[8:-1]
            folders_temp = folders_temp.split(",")
            for folder in folders_temp:
                folder = folder.strip()
                out_folders.append(folder)

    return system_path, out_folders


def create_yr_dir(root, yr):
    year_dir = P(path.join(root, yr))

    if year_dir.exists():
        pass
    else:
        year_dir.mkdir()

    return year_dir


def create_job_dir(root, prefix, number):
    job = root.joinpath(prefix + "-" + number)

    if job.exists():
        print('That job number already exists')
    else:
        job.mkdir()
    return job


def create_job_folders(root, folder_list):
    for folder in folder_list:
        item = root.joinpath(folder)
        if not item.exists():
            item.mkdir()


time = datetime.utcnow()
year = str(time.year)
month = time.month
if month < 10:
    month = "0" + str(month)
else:
    month = str(month)
yy_mm = year[2:] + "-" + month

# Set up the system variables
sys_path, folders = setup_sys()


def setup_job(job_number):
    year_folder = create_yr_dir(sys_path, year)
    job_root = create_job_dir(year_folder, yy_mm, job_number)
    create_job_folders(job_root, folders)

if __name__ == '__main__':

    # make the top level folders
    year_folder = create_yr_dir(sys_path, year)
    job_root = create_job_dir(year_folder, yy_mm, argv[1])
    create_job_folders(job_root, folders)
