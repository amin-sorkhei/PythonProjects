import re
import os
import commands
import re
def main():
    result = open('key_words_bag.txt', 'w')
    failure = open('failure.txt', 'w')
    address = '/home/sorkhei/Desktop/LDAPapers/JMLR/Preceedings'
    os.chdir(address)
    sub_directory = os.listdir(address)
    numOfPapers = 0
    numOfFauilures = 0
    for directory in sub_directory:
        path = os.path.join(address, directory)
        # print 'I am here ' + path
        os.chdir(path)
        file_names = os.listdir(path)
        pdf_file_names = [f for f in file_names if f.endswith('.pdf')]
        cmd = 'pdftotext -l 3 '
        for pdf_file_name in pdf_file_names:
            numOfPapers += 1
            status, text = commands.getstatusoutput(cmd + pdf_file_name + ' -')
            match = re.findall(r'[K|k]eywords\:\s([\w|\W]+?)\n+1', text)
            if match:
                words = match[0].replace('\n', ' ')
                result.write(os.path.join(path, pdf_file_name) + '=====>' + '\n')
                result.write('\n'.join([wrd.strip() for wrd in words.split(',')]) + '\n')
            else:

                failure.write(os.path.join(path, pdf_file_name) + '\n')
                numOfFauilures += 1

    print 'num of papers is ' + str(numOfPapers)
    print 'Number of fauilures is ' + str(numOfFauilures)
if __name__ == '__main__':
    main()