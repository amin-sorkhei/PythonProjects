import requests
from bs4 import BeautifulSoup
from urlparse import urljoin
import os
from pattern.web import URL


def proper_name(url):  # returns the last part of the url as the name
    parts = url.split('/')
    return parts[-1]


def web_scrap(base_url):

    html = requests.get(base_url)
    soup = BeautifulSoup(html.content)
    content = soup.find_all('div', {'id': 'content'})
    tag_soup = BeautifulSoup(str(content))
    links = tag_soup.find_all('a')
    links.pop()  # the last one is useless

    section_links = []
    section_links_dictionary = {}

    for link in links:
            section_links.append(urljoin(base_url, link.get('href')))
            section_links_dictionary[link.text] = urljoin(base_url, link.get('href'))

    # print '\n'.join(section_links)
    # os.mkdir('/home/sorkhei/JMLR')
    # os.chdir('/home/sorkhei/JMLR')
    for link in section_links[0:1]:
        print 'downloading from : ' + str(link)
        section_html = requests.get(link)
        section_soup = BeautifulSoup(section_html.content)
        section_content_links = BeautifulSoup(str(section_soup.find('div', {'id': 'content'})))
        section_download_links = section_content_links.find_all('a')
        # in order to download only pdf files
        section_download_pdf_links = [link for link in section_download_links if str(link.get('href')).endswith('pdf')]
        print len(section_download_pdf_links)
        for link in section_download_pdf_links:
            print base_url
            print link.get('href')
            url = urljoin(base_url, link.get('href'))
            print url

def main():
    print 'hello'
    base_url = 'http://www.jmlr.org/papers/'
    web_scrap(base_url)

if __name__ == '__main__':
    main()