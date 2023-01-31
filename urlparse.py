#https://www.ics.uci.edu,https://www.cs.uci.edu,https://www.informatics.uci.edu,https://www.stat.uci.edu
import re
from urllib.parse import urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu",".stat.uci.edu"]
    try:
        parsed = urlparse(url)
        
        for d in domains:
            if d in parsed.netloc:   
                if parsed.scheme not in set(["http", "https"]):
                    return False
                return not re.match(
                    r".*\.(css|js|bmp|gif|jpe?g|ico"
                    + r"|png|tiff?|mid|mp2|mp3|mp4"
                    + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                    + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                    + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                    + r"|epub|dll|cnf|tgz|sha1"
                    + r"|thmx|mso|arff|rtf|jar|csv"
                    + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())
            else:
                continue
        return False

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def main():

    urls = ["https://www.ics.uci.edu", "https://www.cs.uci.edu", "https://www.informatics.uci.edu", "https://www.stat.uci.edu"]

    links = set()
    for url in urls:
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for link in soup.find_all('a'):
            #print(link.get('href'))
            if is_valid(link.get('href')):
                #print(link.get('href'))
                links.add(urldefrag(link.get('href'))[0])
    #print(links)
    for link in links:
        print(link)
    print("Total links: ", len(links))
    


if __name__ == "__main__":
    main()