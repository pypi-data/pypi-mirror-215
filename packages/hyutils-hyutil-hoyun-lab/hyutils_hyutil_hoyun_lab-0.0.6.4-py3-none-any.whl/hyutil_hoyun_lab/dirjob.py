# author:	nohgan.im

# import the necessary packages
import os

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def files_ext(path, ext):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            extension = os.path.splitext(file)[1]
            if extension == ext:
                yield file

def files_ext_sub(path, ext):
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = os.path.splitext(file)[1]
            if extension == ext:
                file_path = os.path.join(root, file)
                yield file_path, root

def dirs(path):
    for file in os.listdir(path):
        if os.path.isdir(os.path.join(path, file)):
            yield file

def get_entry_count(path, ext):
    total_files = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(ext):
                total_files += 1

    return total_files
    
def listfiles(rootdir):
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isfile(d):
            yield(d)
        if os.path.isdir(d):
            listfiles(d)