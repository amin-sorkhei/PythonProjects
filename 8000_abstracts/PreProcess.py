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
    ''' less_frequent_words, _ = ReKnow.least_frequent_words_finder('4-Stems.txt', 4)
    print len(less_frequent_words)
    dic = open('stem->words_Dictionary.pic')
    stem_word_dic = pickle.load(dic)
    less_than_4_real_words = []
    for word in less_frequent_words:
        less_than_4_real_words += stem_word_dic[word]
    print less_than_4_real_words '''
    stem_word_dictionary = pickle.load(open('stem->words_Dictionary.pic'))
    freq_dic = open('RawFrequency.pic')
    raw_frequency_dic = pickle.load(freq_dic)
    # print raw_frequency_dic
    sorted_raw_count_list = sorted(raw_frequency_dic.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_raw_count_list)
    with open('frequency_of_all_words.txt', 'w') as test:
        for tuple in sorted_raw_count_list:
            test.write(' '.join(stem_word_dictionary[tuple[0]]) + ' : ' + str(tuple[1]) + '\n')
if __name__ == '__main__':
    main()