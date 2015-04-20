def main():
    unmatched_words = []
    word_family_dic = {}
    words = open('all.txt', 'r').readlines()
    words = list(set(map(lambda x: x.lower().strip(), words)))
    print 'Number of Unique words in the bag'
    print len(words)
    one_words = filter(lambda x: len(x) > 2 and len(x.split(' ')) == 1 and '-' not in x, words)
    one_words.sort(lambda x, y: -cmp(len(x), len(y)))
    print one_words
    compound_words = list(set(words) - set(one_words))
    print 'Number of one_word keywords'
    print len(one_words)
    for key in one_words:
        found = filter(lambda x: key in x, compound_words)
        if not found:
            unmatched_words.append(key)
        else:
            word_family_dic[key] = found
            compound_words = list(set(compound_words) - set(found))

    '''print 'Number of unmatched key_words'
    print len(unmatched_words)
    print 'Unmatched key_words: '
    print unmatched_words
    matched_words = list(set(one_words) - set(unmatched_words))
    print 'Number of matched key_words'
    print len(matched_words)
    print 'matched key_sords: '
    print matched_words
    print 'Number of leftovers'
    print len(compound_words)
    print 'leftovers'
    print compound_words'''
    #print word_family_dic.items()
    with open('dictionary.txt', 'w') as result:
        map(lambda item: result.write(item[0] + '\t->\t' + ' , '.join(item[1]) + '\n'), word_family_dic.items())
if __name__ == '__main__':
    main()
