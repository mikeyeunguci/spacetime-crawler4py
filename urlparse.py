#https://www.ics.uci.edu,https://www.cs.uci.edu,https://www.informatics.uci.edu,https://www.stat.uci.edu
import re
from urllib.parse import urlparse, urldefrag, urljoin
import urllib.robotparser
import requests
from utils import download
from bs4 import BeautifulSoup

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu",".stat.uci.edu"]
    try:
        parsed = urlparse(url)
        
        rp = urllib.robotparser.RobotFileParser()
        
        rp.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")

        rp.read()
        print("Sitemaps :", rp.site_maps())
        if rp.can_fetch("*", url):
            print("Crawlable", url + "/robots.txt")
        #parsed.netloc

        
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

    urls = ["https://archive.ics.uci.edu/ml/datasets.php?format=&task=cla&att=mix&area=soc&numAtt=10to100&numIns=less100&type=text&sort=taskUp&view=table"]
    # , ".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu",".stat.uci.edu", "https://www.stat.uci.edu/wp-sitemap.xml"
    links = []
    for line in urls:
        #html_content = requests.get(url).text
        parsed = urlparse(line)
        
        #soup = BeautifulSoup(html_content, 'xml')
        line = "https://www.ics.uci.edu/honors/degrees/policies/sao/computing/account/resources/courses/advising/lmao.php"

        print(parsed.query)
        print(str(parsed.path).split('/')[:-1])
        print(line.split('/')[3:-1])
        print(str(parsed.path).split('/')[-1])
        print(line.split('/'))

        if set(str(parsed.path).split('/')[1:-1]).issubset(set(line.split('/')[3:-1])) and parsed.netloc in line and str(parsed.path).split('/')[-1] == line.split('/')[-1]:
            print("not valid")
        else:
            print("valid")
        # rp = urllib.robotparser.RobotFileParser()

        # rp.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
        # rp.read()
        # print(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
        # print("Sitemaps :", rp.site_maps())


        #for link in soup.find_all("loc"):
            #print(link.text)
        # for link in soup.findAll('a'):
        #     parsed = urlparse(urldefrag(link.get('href'))[0])
        #     if parsed.netloc == "":
        #         parsed = urljoin(url, urldefrag(link.get('href'))[0])
        #         print(parsed)
        #         if is_valid(url):
                    
        #             links.append(parsed)
        #     else:
        #         links.append(urldefrag(link.get('href'))[0])
    # for link in links:
    #     print(link)
    print("Total links: ", len(links))
    
if __name__ == "__main__":
    main()