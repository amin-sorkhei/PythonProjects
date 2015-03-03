__author__ = 'sorkhei'
from xml.etree.ElementTree import parse

def main():
    tree = parse('input.xml')
    root = tree.getroot()
    f = open('all_abstract.txt','w')
    for article in root.findall('article'):
       title = article.find('title').text
       abstract = article.find('abstract').text
       f.write(title+' ' + abstract + '\n')
    f.close()
if __name__ == '__main__':
    main()
