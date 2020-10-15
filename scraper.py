from bs4 import BeautifulSoup
import requests


def getWebsiteLinks(url, keyword, depth):
    links = []
    # gets plain html from the website as text
    html_page = requests.get(url).text
    # only works if the keyword is found in the website
    if(keyword in html_page):
        inputFile = open('links.txt', 'a')
        inputFile.write(f'Link: {url}, Keyword: {keyword}, Depth: {depth}\n')
        inputFile.close()
        soup = BeautifulSoup(html_page, "html.parser")
        # parses all the url and organizes them in an array
        if(depth == 'Initial Link'):
            depth = -1
        for link in soup.findAll('a'):
            if 'http' in str(link.get('href')):
                links.append(str(link.get('href')))
        links = list(dict.fromkeys(links))
    return (links, depth + 1)
