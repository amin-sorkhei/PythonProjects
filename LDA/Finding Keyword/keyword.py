import re
import os
import commands

def main():
    address = '/home/sorkhei/Desktop/LDAPapers/JMLR/Papers/v1'
    os.chdir(address)
    file_names = os.listdir(address)
    file_names = [f for f in file_names if f.endswith('.pdf')]
    print '\n'.join(file_names)
    cmd = 'pdftotext -l 2 -enc UTF-8 '
    for file in file_names:
        (status, output) = commands.getstatusoutput(cmd + file)


if __name__ == '__main__':
    main()