import re


def main():
    lines = open('unique.txt', 'r').readlines()
    lines = list(set(lines))
    keywords = [line.strip() for line in lines]
    one_word = [word for word in keywords if len(word.split(' ')) == 1]
    spaced_keywords = [' ' + word + ' ' for word in keywords]
    '''
    abbreviations = [wrd for wrd in one_word if len(wrd) <= 4]

    abbreviations.remove('tree')
    abbreviations.remove('clop')
    abbreviations.remove('dice')
    abbreviations.remove('huge')
    abbreviations.remove('spam')
    abbreviations.remove('bias')
    abbreviations.remove('test')

    with open('abbreviations.txt', 'w') as result:
        result.write('\n'.join(abbreviations))
    refined_keywords = [words for words in keywords if words not in abbreviations]
    with open('refined_keywords.txt', 'w') as result:
        result.write('\n'.join(refined_keywords))
    '''
    keywords_dic = dict([(k, []) for k in one_word])
    for word in one_word:
        for keyword in spaced_keywords:
            if re.search('\W+' + word + '[s]*\W+', keyword) and word != keyword.strip():
                keywords_dic[word].append(keyword)
        if not keywords_dic[word]:
            print word + ' is not matched'



    with open('dic.txt', 'w') as result:
        for k in [key for key in sorted(keywords_dic.keys()) if keywords_dic[key]]:
            result.write(k + '\t=>\t' + ', '.join(keywords_dic[k]) + '\n')

if __name__ == '__main__':
    main()