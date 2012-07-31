#!/usr/bin/env python
#file = extcopy.py
#programmer = metulburr
#purpose = After downloading numerous torrents...will copy ALL (of list filetype) to home/<user>/Copy_Torrent
    #and create if not exists home/<user>/Copy_Torrent
    #to not have to manuelly copy/paste all subdirectories and filter out junk from torrent
#warning = currently programmed to copy ALL files of filetype of the directory tree chosen

__version__ = 1.04
#added: will unzip zip files to home containing filetypes and copying them to dest
import os
import sys
import shutil
import zipfile

filetype = ['.avi', '.xvid', '.mp4', '.mkv', '.mp3', '.m4v', '.iso', '.divx']

#-------------change filetype v
def print_filetype(filetype):
    print('Current filetypes are: ', filetype)
    
def add_filetype(filetype):
    print_filetype(filetype)
    user_filetype = input('Add new filetype to search: ')
    if user_filetype not in filetype: #check if filetype already in list filetype
        filetype.append(user_filetype)
    else:
        print('filetype already exists')
    return filetype
    
def delete_filetype(filetype):
    print_filetype(filetype)
    if filetype == []: #stop from clear and then delete with no exit
        print('There is nothing to delete\n')
    else:
        try: #if in filetype
            user_filetype = input('Delete filetype from search: ')
            filetype.remove(user_filetype)
        except ValueError: #if not in filetype
            if user_filetype not in filetype:
                print(user_filetype, 'is not in', filetype)
                delete_filetype(filetype)
    return filetype
            
def clear_filetype(filetype):
    filetype = []

def menu(filetype):
    print_filetype(filetype)
    print('1) Continue')
    print('2) Add a new filetype to search')
    print('3) Delete a filetype to search')
    print('4) Clear all filetypes')
    changefile = input()
    if changefile == '2':
        filetype = add_filetype(filetype)
        menu(filetype)
    elif changefile == '3':
        filetype = delete_filetype(filetype)
        menu(filetype)
    elif changefile == '4':
        filetype = []
        menu(filetype)
    else: #leave default
        pass
    return filetype

filetype = menu(filetype)
#-------------change filetype ^

#-------------change path/dest directory v

dest_name = 'ExtCopy'
path = os.environ['HOME'] #name start location / can change
dest = os.environ['HOME'] + os.sep + dest_name #name file, name destination
home = os.environ['HOME'] #home/stays home

def start_dir():
    user_path = input('Type new start path\n')
    if os.path.exists(user_path):
        return user_path
    else:
        print(user_path, 'does not exist')
        return None

rerun = True
while rerun is True:
    
    print('\nCurrent start path', path)
    print('Current destination: ', dest)
    print('1) Continue')
    print('2) Change start path')
    print('3) Change destination directory name', dest_name)
    #print('4) Change destination')
    
    changedir = input()
    
    if changedir == '2':
        user_path = start_dir()
        if user_path is None:
            continue
        else:
            path = user_path
    elif changedir == '3':
        dest_name = input('Type new name for folder\n')
        dest = os.environ['HOME'] + os.sep + dest_name # change dest_name in dest
    else: 
        rerun = False

#-------------change path/dest directory ^


if not os.path.isdir(dest): #if it does not exist
    os.mkdir(dest) #make directory
    print('Creating directory', dest)

print('-----')
print('walking through', path, 'and copying', filetype, 'files to', dest)
print('-----')

import os
import zipfile
import shutil

filetype = ['.avi', '.xvid', '.mp4', '.mkv', '.mp3', '.m4v', '.iso']

copylist = []
top_path = path

for (path, dirs, files) in os.walk(top_path):
    #print('path is', path)
    for dir in dirs:
        #print('dirs are', dir)
        pass
    for filed in files:
        #print(filed)
        #if zipfile.is_zipfile(filed):
        try: #search zips
            fullpath = path + os.sep + filed
            zip = zipfile.ZipFile(fullpath)
            for name in zip.namelist():
                for ext in filetype:
                    if name.endswith(ext):
                        if fullpath not in copylist:
                            print('extracting zip', filed, '\nfrom', path, '\n---')
                            zip.extractall(top_path)
                            #zip.extract(name, path=top_path)
                            copylist.append(path + os.sep + name)
        except zipfile.BadZipFile: #if file not a zip
            pass
        except IOError: #if no such directory
            pass

for (path, dirs, files) in os.walk(top_path):
    for filed in files:
        for ext in filetype: #search files
            if filed.endswith(ext):
                fullpath = path + os.sep + filed
                if fullpath not in copylist:
                    print('found', filed, '\nfrom', path, '\n---')
                    copylist.append(fullpath)

copyname = []
for index in copylist:
    #print('copylist is', index)
    #print('files are', os.path.split(index)[1])
    
    filename = os.path.split(index)[1]
    if filename not in copyname:
        if filename not in dest:
            #if not filecmp.cmp(filename, copyname):
            try:
                print('copying', filename, 'to', dest)
                shutil.copy(index, dest)
            except:
                pass

print("Program complete!")
