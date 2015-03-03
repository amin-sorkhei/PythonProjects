__author__ = 'sorkhei'
# version 0.0.0
# This is a package developed for ReKnow project at Helsinki Institute for Information Technology
import re
import os
from nltk.corpus import stopwords
from nltk import PorterStemmer
from collections import Counter
import csv
import operator
import pickle


# ---------------------------------------------------------------------------------------------
# This is a DEPENDENT function used to save a dictionary as .dic file using pickle module
# input: a name as the name of the output file and a python object to save
# output: pickled file called output_file_name.pic
def pickle_my_stuff(output_file_name, python_object):
    with open(output_file_name + '.pic', 'w') as f:
        pickle.dump(python_object, f)


# ---------------------------------------------------------------------------------------------
# This is a DEPENDENT function used to save a dictionary as a csv file
# input: a name as the name of the output file and a dictionary to save
# output: a csv file called dictionary.csv
def csv_writer(name, input_dictionary):
    writer = csv.writer(open(name + '.csv', 'w'))
    for key in sorted(input_dictionary.keys()):
        writer.writerow([key, input_dictionary[key]])


# ---------------------------------------------------------------------------------------------
# This is an INDEPENDENT function to read the raw data from xml files from the given directory
# This function reads all the xml files in the specified input_address and creates an
# in the project directory
# input: raw xml files containing all the data
# output: a file containing topic + abstract called ALL_ABSTRACTS.txt
def file_reader(input_address):
    result = open('1-ALL_ABSTRACTS.txt', 'w')
    all_files = os.listdir(input_address)
    for item in all_files:
        absolute_address = os.path.join(input_address, item)  # creates the valid address of the xml files
        if absolute_address.endswith('xml'):  # in order only to process xml files
            current_file = open(absolute_address, 'rU')
            raw_text = current_file.read()
            edited_text = extract_title_abstract(raw_text)
            # edited_text uses extract_title_abstract(text) function to process the file
            result.write(edited_text)

    print' ''ALL_ABSTRACTS.txt'' was created successfully'
    result.close()


# ---------------------------------------------------------------------------------------------
# This is a DEPENDENT function used in file_reader function
# This function retruns a String containing title and abstract in a line which is extracted from xml input
# 'text' contains the xml file with all tags available
# input: some text with <tags>
# output: a text where abstracts and topics are returned
def extract_title_abstract(text):
    match_title = re.findall(
        r'<title>\s*([\W\w\n]*?)\s*</title>[\W\w\n]*?<abstract>\s*([\W\w\n]*?)\s*</abstract></arXiv>', text)
    edited_text = ''  # contains the final version of text#
    assert match_title
    if match_title:
        for item in match_title:
            edited_text += re.sub(r'\n+', ' ', item[0]) + ' ' + re.sub(r'\n+', ' ', item[1]) + '\n'
            # in order to eliminate \n character in abstract and title if there is any
    else:
        exit('No regEx found, there is something wrong in document')
    return edited_text


# ---------------------------------------------------------------------------------------------
# This is an INDEPENDENT functions
# this function gets rid of the latex formulas in the text, it receives a text file
# and replaces latex formulas with nothing
# input: file containing latex formulas
# output: a file free of latex formulas called NoFormulaAbstract.txt
def remove_latex(input_file_name):
    read = open(input_file_name, 'ru')  # opens the given file
    write = open('2-NoFormulaAbstract.txt', 'w')  # creates the new file for the output
    lines = read.readlines()  # reads the input file line by line, each line contains title and the abstract
    for line in lines:
        line = re.sub(r'(\-)+?', ' ', line)
        line = re.sub(r'\\emph', ' ', line)
        line = re.sub(r'\\cite\{.*?\}', ' ', line)
        line = re.sub(r'\\citep\{.*?\}', ' ', line)
        line = re.sub(r'&quot;', ' ', line)
        line = re.sub(r'\$.*?\$', ' ', line)  # to remove LateX formulas
        line = re.sub(r'\(.*?\)', ' ', line)  # to remove whatever comes between parenthesis
        line = re.sub(r'\[.*?\]', ' ', line)  # to remove whatever comes between square brackets
        line = re.sub(r'[^(\s|\w)]', ' ', line)  # to remove non-space and non-word characters
        line = re.sub(r'\d+\)*', ' ', line)  # to remove numbers
        line = line.lower()  # change all the letters to lower case ones
        write.write(line)  # Finally writes the edited text into the file
    read.close()
    write.close()
    print' ''NoFormulaAbstract.txt'' was created successfully'


# ---------------------------------------------------------------------------------------------
# This is an INDEPENDENT functions
# this function gets rid of stop words in the text, it receives a text file
# and replaces stopwords with nothing
# input: file containing stopwords
# output: a file free of stopwords called 'Non_stop.txt'
def remove_stop_words(file_name):
    input_file = open(file_name, 'rU')  # the file name where there are stopwords
    output_file = open('3-Non_stop.txt', 'w')
    stop_words = stopwords.words('english')
    for line in input_file.readlines():
        non_stops = [w.lower() for w in line.split() if (w not in stop_words and len(w) > 2)]
        # removes words which belong to stop words or their length is less than 4
        output_file.write(' '.join(non_stops))
        output_file.write('\n')
    input_file.close()
    output_file.close()
    print' ''Non_stop.txt'' was created successfully'


# ---------------------------------------------------------------------------------------------
# This is an INDEPENDENT function to read the files containing non_stop words
# input: The file where all non stop words are removed
# output: This function returns two files
# 1- Stems.txt where the stemmizd version of the text is stored
# 2- stem_word.txt where the stem and the corresponding text
# Additionally a dictionary containing the stem and the corresponding words is returned
# Additionally it also creates stem->words_Dictionary.csv dictionary
# Additionally it also saves the dictionary in a file called stem->words_Dictionary.pic so other modules
# can access the dictionary independently if needed
def find_stems(file_name):
    input_file = open(file_name, 'rU')
    output_file_stems = open('4-Stems.txt', 'w')
    output_file_stems_words = open('5-stem_word.txt', 'w')
    porter = PorterStemmer()
    stem_word = {}  # The dictionary contains the stem words
    for line in input_file.readlines():
        words = []  # contains the filtered words of the current abstract
        stems = []
        for w in line.split():
            match = re.search(r'[_|\W]*([a-zA-Z]+)[_|\W]*',
                              w)  # This is the final filter where some words my be dropped
            tmp = match.group(1)
            if len(tmp) > 3:
                words.append(tmp)  # if the words passes the filter it appends to tmp
        for w in words:
            stem = porter.stem(w)
            if stem not in stem_word:
                stem_word[stem] = [w]
            elif w not in stem_word[stem]:
                stem_word[stem].append(w)
            stems.append(stem)

        output_file_stems.write(' '.join(stems))
        output_file_stems.write('\n')

    bindings = ''  # a temporary string to append all stems and corresponding words
    for key in sorted(stem_word.keys()):
        bindings += key + '\t' + ' '.join(stem_word[key]) + '\n'
    output_file_stems_words.write(bindings)
    pickle_my_stuff('stem->words_Dictionary', stem_word)
    input_file.close()
    output_file_stems.close()
    output_file_stems_words.close()
    print" 'Non_stop.txt' was created successfully "
    csv_writer('stem->words_Dictionary', stem_word)
    return stem_word


# ---------------------------------------------------------------------------------------------
# This is an INDEPENDENT function to to find the least frequent words in a given file (preferably after stemming)
# input: the input file name containing the stemmized text and an integer called limit as a threshold to find
# the less frequent words
# output: a list which contains less frequent words and raw frequency dictionary (less_frequent_words,raw_frequency_dic)
# Additionally this method creates a dictionary containing the frequency of each stem in the text called RawFrequency
# and write that to RawFrequency.csv
# Additionally a dictionary file called RawFrequency.pic is created for independent use by other modules

def least_frequent_words_finder(file_name, limit):
    inputFile = open(file_name, 'rU')
    words = [x for x in inputFile.read().split()]  # loads all the words in the given file
    raw_frequency_dic = Counter(words)  # creates a dictionary based on the frequency of each word
    descending_words = raw_frequency_dic.most_common()[::-1]  # changes the dictionary into a list and reverses that
    raw_frequency_dic = dict(raw_frequency_dic)
    less_frequent_words = []
    for (word, frequency) in descending_words:
        if frequency < limit:
            less_frequent_words.append(word)
        else:
            break
    csv_writer('RawFrequency', raw_frequency_dic)
    pickle_my_stuff('RawFrequency', raw_frequency_dic)
    inputFile.close()
    return less_frequent_words, raw_frequency_dic


# ---------------------------------------------------------------------------------------------
# This is an INDEPENDENT function to find the the number documents contain a each word in the dictionary
# input: the input file name and an integer called limit as a threshold to find the most frequent words
# output: the out put is a tuple which contains word_per_doc_count and word_per_doc_freq(percentage) and finally a
# sorted list of most frequent words in the document (word_per_doc_count,word_per_doc_freq,sorted_word_per_doc_freq_list)
# Additionally it writes the dictionaries to word->doc.csv and word->doc_freq.csv
# Additionally it saves the dictionaries as word->doc.pic and word->doc_freq.pic for independent use by other modules
def doc_word_frequency(file_name):
    with open(file_name) as inputFile:
        lines = inputFile.readlines()
        number_of_documents = len(lines)
        word_per_doc = {}  # a dictionary contains all the word per doc frequency
        for line in lines:
            words = set(line.split())  # gets rid of the repetitive words in a document
            for word in words:
                if word in word_per_doc:
                    word_per_doc[word] += 1
                else:
                    word_per_doc[word] = 1

    word_per_doc_freq = {word: freq * 100.0 / number_of_documents for word, freq in (word_per_doc.items())}
    csv_writer('word->doc', word_per_doc)
    csv_writer('word->doc_freq', word_per_doc_freq)
    sorted_word_per_doc_freq_list = sorted(word_per_doc_freq.items(), key=operator.itemgetter(1), reverse=True)
    pickle_my_stuff('word->doc', word_per_doc)
    pickle_my_stuff('word->doc_freq', word_per_doc_freq)
    return word_per_doc, word_per_doc_freq, sorted_word_per_doc_freq_list


