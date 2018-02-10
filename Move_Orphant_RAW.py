#
# This script moves raw files of type NEF and CR2 which do not have
# an coresponding 'JPG' to path_in\delete. The 'JPG' may be corrected
# and therefore have an extended filename looking something like
# -k, -k1. The script will recognize a JPG if the filname equals the
# filename of a raw file the jpg file may have any addition at the end
# of it.
#
# example:
# orignial fielname DSC2334.jpg
# extended filename DSC2334-corrected.jpg
#
# !!! Use this script on your own risk !!!
#
# Author Eagle Ed
#
# Version History
# 2018-02-10	Version 1.0
#
import os
import sys
from os import walk
import getopt
import fnmatch
import shutil

# add more raw types to your need
list_of_raw_type = ['.nef', '.cr2']
dst_folder = 'to_delete'

print ('Raw format supported: '),
for element in list_of_raw_type:
    print(element),
print ('')


def main(argv):
    # verify the arguments
    path_in = ''
    all_args = sys.argv[1:]
    print '\nall_args ',
    print all_args
    print '\n'
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
    print ''
    print path_in + '\n'
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


def check_for_raw(file_extension):
    flag_raw = 'false'
    if file_extension.lower() in list_of_raw_type:
        flag_raw = 'true'
    return flag_raw


def search_jpg(file_name, filelist):
    flag_jpg_exists = 'false'
    for files in filelist:
        search_string = file_name + '*.jpg'
        if fnmatch.fnmatch(files, search_string):
            flag_jpg_exists = 'true'
    return flag_jpg_exists


def move_orphant_raw(path_in, filename, dst_dir):
    file_to_move = os.path.join(path_in, filename)
    file_in_dst_dir = os.path.join(dst_dir, filename)
    if os.path.exists(file_in_dst_dir):
        os.remove(file_in_dst_dir)
    shutil.move(file_to_move, dst_dir)


# store cli arguments
path_in = main(sys.argv[1:])

# dst_dir = directory where orphand raw are moved to
dst_dir = os.path.join(path_in, dst_folder)

filelist = list_files_only(path_in)
orphan_count = 0

for datei in filelist:
    flag_raw = 'false'
    # split datei into file_name and file_extension
    file_name, file_extension = os.path.splitext(datei)
    # check wheter its a raw file or not
    result = check_for_raw(file_extension)
    if result == 'true':
        # if so check if there is a jpg for it
        result = search_jpg(file_name, filelist)
        if result == 'false':
            # check if the dst_dir exists
            if os.path.exists(dst_dir):
                if not os.path.isdir(dst_dir):
                    create_path(dst_dir)
            else:
                create_path(dst_dir)
            # if not move the raw file to the folder to_delete
            print('file ' + file_name + file_extension + ' is orphand')
            move_orphant_raw(path_in, datei, dst_dir)
            orphan_count += 1

print
print 'Done - %s orphand raw moved to folder to_delete' % orphan_count
