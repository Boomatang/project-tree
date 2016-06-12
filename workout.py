from os import walk, path



def find_objects(root):

    path_files = []
    for root, dirs, files in walk(root):
        for file in files:
            file = path.join(root, file)
            path_files.append(file)
        for dir in dirs:
            dir = path.join(root, dir)
            path_files.append(dir)
    return path_files


if __name__ == '__main__':
    path_root = "/home/boomatang/temp/project-lib"
    paths = find_objects(path_root)
    for i in paths:
        print(i)
