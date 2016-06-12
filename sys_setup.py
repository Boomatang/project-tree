from os import path
from pathlib import Path as P
from datetime import datetime


def setup_sys():
    sys_path = ''
    out_folders = []
    archive = ''
    required_path = ''
    files = []
    with open("sys.conf", 'r') as f:
        content = f.readlines()
        f.close()

    for line in content:
        if line[0:10] == "jobs_path=":
            sys_path = line[10:-1]
        elif line[0:13] == "archive_path=":
            archive = line[13:-1]
        elif line[0:8] == "folders=":
            folders_temp = line[8:-1]
            folders_temp = folders_temp.split(",")
            for folder in folders_temp:
                folder = folder.strip()
                out_folders.append(folder)
        elif line[0:19] == 'required_docs_path=':
            required_path = line[19: -1]
        elif line[0:9] == "document=":
            file_names = line[9:-1]
            file_names = file_names.split(',')
            with open("sys.conf", 'r') as doc:
                doc_lines = doc.readlines()
                doc.close()
            for name in file_names:
                name = name.strip()
                name = name.split(':')
                for lines in doc_lines:
                    if lines[0:len(name[0]) + 1] == name[0] + "=":
                        x = lines[len(name[0]) + 1: -1]
                        x = path.join(x, name[1])
                        files.append(x)

    return sys_path, out_folders, archive, required_path, files

system_path, folders, job_archive, required, files = setup_sys()


def create_yr_dir():
    year_dir = P(path.join(system_path, str(datetime.utcnow().year)))
    archive_dir = P(path.join(job_archive, str(datetime.utcnow().year)))

    if year_dir.exists():
        pass
    else:
        year_dir.mkdir()
        archive_dir.mkdir()


def create_job_folders(root):
    for folder in folders:
        item = root.joinpath(folder)
        if not item.exists():
            item.mkdir()

if __name__ == '__main__':
    system_path, folders, job_archive, required, files = setup_sys()

    print("Jobs Path: " + system_path)
    print("Archive Path: " + job_archive)
    print("Required Document Paths: " + required)
    print("List of folders: ", end='')
    for i in folders:
        print(i, end=', ')
    print()
    print('Files to be added:')
    for i in files:
        print(i)
    print()

