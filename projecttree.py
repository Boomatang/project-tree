from os import path
from pathlib import Path as p
from datetime import datetime
import sys
from JobFolders import setup_job


folders_list = ["testing", "app", "invoices", "pictures"]
year = str(datetime.utcnow().year)


def data_input():
    clint_name = input("Clint Name: ")
    desc = input("Project name: ")
    number = input("Project Number: ")
    return clint_name, desc, number


def make_required_folders(top_level, folders):
    top_level = str(top_level)

    for folder in folders:
        print("Creating Folder " + folder)
        folder = p(path.join(top_level, folder))
        if not folder.exists():
            folder.mkdir()


clint = "Clint name test"
project_name = "Test Project Name"
project_number = "TestProject Number"
sys_path = ""

with open("sys.conf", 'r') as f:
    content = f.readlines()
    f.close()

print(content)

for line in content:
    if line[0:5] == "path=":
        sys_path = line[5:-1]


def check_number():
    project_number_list = path.join(sys_path, "project Numbers.txt")

    with open(project_number_list, 'r') as text:
        lines = text.readlines()
        text.close()
        if project_number + "\n" in lines:
            print("Project number is already in use.")
            print("System is exiting")
            sys.exit(0)
        else:
            with open(project_number_list, 'a') as write:
                write.write(project_number + "\n")
                write.close()


def create_folders():
    clint_path = p(path.join(sys_path, clint))
    if not clint_path.exists():
        print("Creating file system...")
        clint_path.mkdir()
    else:
        print("clint path exists")

    year_path = p(path.join(str(clint_path), year))
    if not year_path.exists():
        year_path.mkdir()

    project = project_number + " - " + project_name
    project_path = p(path.join(sys_path, clint, year, project))

    if not project_path.exists():
        print("Creating Project...")
        project_path.mkdir()
    else:
        print("Project path exists")

    make_required_folders(project_path, folders_list)


def summary():
    print("Current Working year is " + year)
    print("Clint Name: " + clint)
    print("Project Name:" + project_name)
    print("Project Number:" + project_number)
    print("System path exists " + str(path.exists(sys_path)))

if __name__ == '__main__':
    clint, project_name, project_number = data_input()
    setup_job(project_number)
    #check_number()
    #create_folders()
    #summary()
