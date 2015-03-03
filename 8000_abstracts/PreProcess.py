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
    #ReKnow.remove_latex('all_abstract.txt')
    #ReKnow.remove_stop_words('2-NoFormulaAbstract.txt')
    ReKnow.find_stems('3-Non_stop.txt')
    less_frequent_words, _ = ReKnow.least_frequent_words_finder('4-Stems.txt',4)
    print len(less_frequent_words)
    dic = open('stem->words_Dictionary.pic')
    stem_word_dic = pickle.load(dic)
    real_words = []
    for word in less_frequent_words:
        real_words += stem_word_dic[word]
    print real_words
    print less_frequent_words
    ReKnow.remove_words('3-Non_stop.txt', real_words)

if __name__ == '__main__':
    main()