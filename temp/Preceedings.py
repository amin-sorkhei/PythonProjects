from bs4 import BeautifulSoup as bsoup
import pattern.web as web
from urlparse import urljoin as join
import re
import os


def scrap_preceeding(base_url):
    homepage_html_content = web.download(base_url)
    homepage_soup = bsoup(homepage_html_content)
    ul_content = homepage_soup.find_all('ul')
    a_content = bsoup(str(ul_content)).find_all('a')
    volume_page_links = []
    for raw_link in a_content:
        volume_page_links.append(join(base_url, raw_link.get('href'))+'/')


    os.chdir('/home/sorkhei/Desktop/LDA-Papers/JMLR/Preceedings/')

    for base_link in volume_page_links[32:]:
        folder_name = base_link.split('/')[-2]
        address = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(address):
            os.mkdir(folder_name)
        else:
            index = 1
            while os.path.exists(address):
                folder_name = base_link.split('/')[-2] + '-' + str(index)
                print folder_name
                address = os.path.join(os.getcwd(), folder_name)
                index += 1
            os.mkdir(folder_name)

        os.chdir(address)


        print '--------------'
        print 'downloading from ' + base_link
        volume_content_soup = bsoup(web.download(base_link)).find_all('div', {'id': 'content'})
        a_content = bsoup(str(volume_content_soup)).find_all('a')
        # print a_content
        pdf_links = [join(base_link, link.get('href')) for link in a_content if str(link.get('href')).endswith('pdf')]
        for download_link in pdf_links:
            if not download_link.endswith('supp.pdf'):
                try:
                    content = web.download(download_link)
                except:
                    print 'link : %s is obsolete' % download_link
                    continue
                f = open(download_link.split('/')[-1], 'wb')
                f.write(content)
                f.close()
        os.chdir('/home/sorkhei/Desktop/LDA-Papers/JMLR/Preceedings/')
def main():
    scrap_preceeding('http://www.jmlr.org/proceedings/')





if __name__ == '__main__':
    main()