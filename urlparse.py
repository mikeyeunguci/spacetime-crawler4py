#https://www.ics.uci.edu,https://www.cs.uci.edu,https://www.informatics.uci.edu,https://www.stat.uci.edu
import re
from urllib.parse import urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

def main():
   # url = urlparse('https://www.ics.uci.edu', allow_fragments=False)
    url = "https://www.ics.uci.edu"
    #link = url[0]
    

    links = []
    print("URL:", url)

    html_content = requests.get(url).text

    soup = BeautifulSoup(html_content, 'html.parser')

    for link in soup.find_all('a'):
        #print(link.get('href'))
        links.append(link.get('href'))
    print(links)


if __name__ == "__main__":
    main()