#
# This script moves raw files of type NEF and CR2 which do not have
# an coresponding 'JPG' to path_in\delete. The 'JPG' may be corrected
# and therefore have an extended filename looking something like
# -k, -k1. The script will recognize a JPG if the filname equals the
# filename of a raw file the jpg file may have any addition at the end
# of it.
# In addition to the raw file, the script removes Dartable files with
# the extension .xmp
# 
# example:
# orignial fielname DSC2334.jpg
# extended filename DSC2334-corrected.jpg
#
# !!! Use this script at your own risk !!!
#
# Author Eagle Ed
#
# Version History
# 2018-02-10	Version 1.0
# 2019-01-13    Version 1.1
#   - remove Darktable files
#
import os
import sys
from os import walk
import getopt
import fnmatch
import shutil
import re


def main(argv):
    # verify the arguments
    path_in = ''
    all_args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:", ["help=", "path="])
    except getopt.GetoptError:
        print 'please use: Delete_Orphant_RAW.py -p <path>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", '--help'):
            print 'usage: Delete_Orphant_RAW.py -p <path>'
            sys.exit()
        elif opt in ("-p", "--path"):
            path_in = arg
    if (path_in == ''):
        print 'please enter: -p <path'
        sys.exit(2)
    return path_in


def list_files_only(in_dir):
    filelist = []
    for (dirpath, dirnames, filenames) in walk(in_dir):
        filelist.extend(filenames)
        break  # prevent walk from diving into the subdirs
    return filelist


def count_files_only(in_dir):
    file_count = 0
    for (dirpath, dirnames, filenames) in walk(in_dir):
        for file in filenames:
            file_count += 1
    return file_count


def create_path(out_path):
    # create the out path
    os.makedirs(out_path)


def check_filetype(file_extension):
    file_type = ''
    if file_extension.lower() in list_of_sidecar_type:
        file_type = 'sidecar'
    elif file_extension.lower() in list_of_raw_type:
        file_type = 'raw'
    return file_type


def search_jpg(file_name, filelist):
    flag_jpg_exists = False
    for files in filelist:
        search_string = file_name + '.*\.jpe?g$'
        found_jpg = re.search(search_string, files, re.IGNORECASE)
        if found_jpg:
            flag_jpg_exists = True
    return flag_jpg_exists


def move_orphant_raw(path_in, filename, dst_dir):
    file_to_move = os.path.join(path_in, filename)
    file_in_dst_dir = os.path.join(dst_dir, filename)
    if os.path.exists(file_in_dst_dir):
        os.remove(file_in_dst_dir)
    shutil.move(file_to_move, dst_dir)


# store cli arguments
path_in = main(sys.argv[1:])

# add more raw types to your need
list_of_raw_type = ['.nef', '.cr2']
list_of_sidecar_type  = ['.xmp', '.pp3','.on1']

print '\nRaw format supported: ',
for element in list_of_raw_type:
    print(element),
print '\nSidecar format supported: ', 
for element in list_of_sidecar_type:
    print(element),
print

dst_folder = 'to_delete'
# dst_dir = directory where orphand  raw and sidecar files are moved to
dst_dir = os.path.join(path_in, dst_folder)
filelist = list_files_only(path_in)
orphant_count = 0
sidecar_count = 0

for datei in filelist:
    flag_raw = False
    # split datei into file_name and file_extension
    file_name, file_extension = os.path.splitext(datei)
    # figure out file typ (none = image type, raw or sidecar)
    file_type = check_filetype(file_extension)
    if file_type == 'raw' or file_type == 'sidecar':
        if file_type == 'sidecar':
            # remove the image type extension (.jpg, .cr2, .nef) from the filename
            file_name = file_name[:len(file_name)-4]
        jpg_found = search_jpg(file_name, filelist)
        if not jpg_found:
            # check if the dst_dir exists
            if os.path.exists(dst_dir):
                if not os.path.isdir(dst_dir):
                    create_path(dst_dir)
            else:
                create_path(dst_dir)
            move_orphant_raw(path_in, datei, dst_dir)
            if file_type == 'sidecar':
                sidecar_count += 1
            elif file_type == 'raw':
                orphant_count += 1


print 'Done\n - %s orphand raw moved to folder to_delete' % orphant_count
print ' - %s orphand sidecar moved to folder to_delete' % sidecar_count
