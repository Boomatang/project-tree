from os import path
from pathlib import Path as p
'''
clint = input("Clint Name: ")
project_name = input("Project name: ")
project_number = input("Project Number: ")
'''

clint = "Clint name test"
project_name = "Test Project Name"
project_number = "TestProject Number"
sys_path = ""

with open("sys.conf", 'r') as f:
    content = f.readlines()

print(content)

for line in content:
    if line[0:4] == "path":
        sys_path = line[5:-1]


clint_path = p(path.join(sys_path, clint))



if not clint_path.exists():
    print("Dir not there Creating...")
    clint_path.mkdir()
else:
    print("clint path exists")


print("Clint Name: " + clint_path.name)
print("Project Name:" + project_name)
print("Project Number:" + project_number)
print("System path exists " + str(path.exists(sys_path)))
