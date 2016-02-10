#
# c.13.py by Hexapetalous on Feb 10, 2016.
# This is a part of C0013. Copyright 2016 Hexapetalous. All rights reserved.
#

# STEP 0 #
def printl(string):
    print(string, end='', flush=True)

printl('Initializing...')
import P0009.btbb as p9b
import P0009.btbbc as p9c
from optparse import OptionParser

# STEP 1 API(s) #
DATA_FILE_PATH = '/home/wan/N_E_I_H version1.0/C0013/233.txt'  # Default path
RESULT_DIR_PATH = '/home/wan/N_E_I_H version1.0/C0013/result'  # Default path
print('[^_^]')

# STEP 2 Parser #
printl('Parsing option parse...')
parser = OptionParser()
parser.add_option('-f', '--file', dest='filename')
(options, args) = parser.parse_args()

# If the arg is pointed out then use the specific one, or use default.
if options.filename is not None:
    DATA_FILE_PATH = options.filename
try:
    RESULT_DIR_PATH = args[0]
except IndexError:
    pass
print('[^_^]')
print('FILE NAME %s' % DATA_FILE_PATH)
print('OUT DIR %s' % RESULT_DIR_PATH)

# STEP 3 Analyze file #
DATA_VERSION = 1
print('Analyzing file...')
print('DATA ENGINE VERSION %d' % DATA_VERSION)
try:
    data_file = open(DATA_FILE_PATH, mode='r')
except FileNotFoundError:
    print('ERROR Can not found file %s.' % DATA_FILE_PATH)
    exit()

root_url = None
root_title = None
info = dict()  # May be discrete.
# noinspection PyUnboundLocalVariable
data_file_lines = [line for line in data_file]
i = 0
finished_line = 0
while i < len(data_file_lines):
    if i >= finished_line:
        print('Finished %d line(s).' % i)
        finished_line += 64
    line = data_file_lines[i]
    if line[0] == '#':  # Comment.
        i += 1  # TODO: This is a ugly and awful design!
        continue
    if line[:4] == 'ROOT':
        root_url = line[5:-1]  # `-1` is for `\n`.
        i += 1
        continue
    if line[:4] == 'TITL':
        root_title = line[5:-1]
        i += 1
        continue
    if line[:2] != 'ID':  # The id line may be commented or broken.
        i += 1
        continue
    my_id = int(line[5:-1])
    single_theme = dict()
    i += 1
    line = data_file_lines[i]
    if line[:4] != 'NAME':
        print('WARN The data file may be broken.')
        print('Can not analyze: ID %d' % my_id)
        print('LINE(follow line)')
        print(line)
        i += 1
        continue
    single_theme['name'] = line[5:-1]
    i += 1
    line = data_file_lines[i]
    if line[:4] != 'HREF':
        print('WARN The data file may be broken.')
        print('Can not analyze: ID %d' % my_id)
        print('LINE(follow line)')
        print(line)
        i += 1
        continue
    single_theme['href'] = line[5:-1]
    info[my_id] = single_theme
    i += 1
print('[^_^]')
print('ROOT URL %s' % root_url)
print('ROOT TITLE %s' % root_title)
print('TOTAL CHILD COUNT %d' % len(info))

# STEP 4 Check #
print('Checking how many you have already got...')
import os
if os.path.isdir(RESULT_DIR_PATH) is False:
    print('ERROR %s is not a dir.' % RESULT_DIR_PATH)
    exit()
dir_name = os.path.join(RESULT_DIR_PATH, root_title.split('_')[0])
if os.path.isdir(dir_name) is False:
    print('A-ha! There is nothing at all!')
    printl('Create containing dir...')
    os.mkdir(dir_name)
    print('[^_^]')

printl('Change dir to %s...' % dir_name)
os.chdir(dir_name)
print('[^_^]')

important_info = dict()
already_had_count = 0
not_have_yet_count = 0
for item in info.values():
    name = item['name']
    file_name = name + '.json'
    if os.path.exists(file_name):
        already_had_count += 1
    else:
        not_have_yet_count += 1
        important_info[name] = item['href']

print('%d exists, %d on the way.' % (already_had_count, not_have_yet_count))
