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
    dest_root_address = '/home/sorkhei/Desktop/LDA Papers/JMLR/Papers'
    os.chdir(dest_root_address)
    for link in section_links[2:]:
        print '----------downloading from : ' + str(link)
        directory_name = str(link).split('/')[-1]
        section_html = requests.get(link)
        section_soup = BeautifulSoup(section_html.content)
        section_content_links = BeautifulSoup(str(section_soup.find('div', {'id': 'content'})))
        section_download_links = section_content_links.find_all('a')
        # in order to download only pdf files
        section_download_pdf_links = [link for link in section_download_links if str(link.get('href')).endswith('pdf')]
        # we are now in a section where odf links of the section are stored in section_download_pdf_links
        os.mkdir(directory_name)
        for pdf_download_link in section_download_pdf_links:
            print os.getcwd()
            sub_directory_address = os.path.join(dest_root_address, directory_name)
            os.chdir(sub_directory_address)
            url = urljoin(base_url, pdf_download_link.get('href'))
            pdf_file_name = str(url).split('/')[-1]
            try:
                pdf_file = requests.get(url)
            except:
                print 'page not found: ' + str(url)

            pdf_file_writer = open(pdf_file_name, 'wb')
            pdf_file_writer.write(pdf_file.content)
            pdf_file_writer.close()

        os.chdir('/home/sorkhei/Desktop/LDA Papers/JMLR/Papers')

def main():
    print 'hello'
    base_url = 'http://www.jmlr.org/papers/'
    web_scrap(base_url)

if __name__ == '__main__':
    main()