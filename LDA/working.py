import operator
from collections import Counter
import matplotlib.pyplot as plt
import scipy as sp
import re
# ---------------------------------------------------------------------------------------------
# This is an INDEPENDENT function to find the the number documents contain a each word in the dictionary
# input: the input file name and an integer called limit as a threshold to find the less frequent words
# output: the out put is a tuple which contains word_per_doc_count and word_per_doc_freq and finally a
# sorted list of most frequent words in the document
# it also writes the dictionaries to word->doc.csv and word->doc_freq.csv

def remove_words(list_of_words):
    f = open('test.txt', 'rU')
    t = open('tmp.txt', 'w')
    text = f.read()
    text = text.lower()
    text = re.sub(r'this|is', '', text)
    text = re.sub(r'this|is', '', text)
    t.write(text)
    f.close()
    t.close()

# -----------------------------------------------------------------------------------------


def main():
    words = ['this', 'is']
    remove_words(words)



if __name__ == '__main__':
    main()






'''def least_frequent_words_finder(file_name, limit):
    with open(file_name) as inputFile:
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
        return less_frequent_words, raw_frequency_dic'''




'''(word_per_doc, word_per_doc_freq, sorted_word_per_doc_freq_list) = doc_word_frequency('4-Stems.txt')
    _, raw_frequency_dict = least_frequent_words_finder('4-Stems.txt', 4)
    word_id = dict(enumerate(sorted(word_per_doc.keys()), start=1))
    x = sorted(word_id.keys())
    y_word_per_doc = [word_per_doc[word_id[k]] for k in x]
    y_raw_frequency = [raw_frequency_dict[word_id[k]] for k in x]

    print x
    print y_word_per_doc
    print y_raw_frequency

    plt.scatter(x, y_word_per_doc,color= 'blue')
    plt.title('Comparison among raw frequency and word_per_doc frequency')
    plt.xlabel('Word Id')
    plt.ylabel('raw count/Count per doc')
    plt.scatter(x, y_raw_frequency,color='orange')
    plt.legend([ 'wrd per doc','raw count'], loc='upper right')
    #plt.autoscale(tight=True)
    plt.grid()
    plt.show()'''