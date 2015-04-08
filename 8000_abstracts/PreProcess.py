import operator

__author__ = 'sorkhei'
from xml.etree.ElementTree import parse
import ReKnow
import pickle


# dahnae ma service shod, reading data from THIS xml file, and may not work on others
def file_reader():
    tree = parse('archive.xml')
    root = tree.getroot()
    f = open('all_abstract.txt', 'w')
    result = ''
    for article in root.findall('article'):
        title = article.find('title').text
        abstract = article.find('abstract').text
        result = title + ' ' + abstract + '\n'
        result = result.encode('ascii', 'ignore')
        f.write(result)

    f.write(result)
    f.close()


def main():
    # Data stored in all_abstract.txt
    # file_reader()
    # ReKnow.remove_latex('all_abstract.txt')
    # ReKnow.remove_stop_words('2-NoFormulaAbstract.txt')
    # ReKnow.find_stems('3-Non_stop.txt')
    less_frequent_words, _ = ReKnow.least_frequent_words_finder('4-Stems.txt', 5)
    print len(less_frequent_words)
    dic = open('stem->words_Dictionary.pic')
    stem_word_dic = pickle.load(dic)
    less_than_5_real_words = []
    for word in less_frequent_words:
        less_than_5_real_words += stem_word_dic[word]

    redundant_words = less_than_5_real_words
    redundant_file = open('redundant-stem.txt', 'r')
    for word in redundant_file.readlines():
        redundant_words += (stem_word_dic[word.strip()])

    with open('final_redundant_words.txt', 'w') as final_file:
        final_file.write('\n'.join(redundant_words))



if __name__ == '__main__':
    main()