import re
from urllib.parse import urlparse, urldefrag

from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    for link in links:
        if(is_valid(link)):
            print(link)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    links = set()
    words_re = re.compile(r'\b\w+\b')
    
    if(resp.status != 200 or resp.error != None):
        return []
    try:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except AttributeError:
        return []

    words = []
    stop_words = []
    
    for word in words_re.findall(soup.text):
        if word.lower() not in stop_words:
            words.append(word.lower())
    print(words)

    with open("Longest.txt", "w+") as Long:
        for line in Long:
            count = line.split()[1]


    with open("visited.txt", "a+") as Visit:
        Visit.write(url)
        Visit.write("\n")

    for link in soup.find_all('a'):
        print(urldefrag(link.get('href'))[0])
        links.add(urldefrag(link.get('href'))[0])

    return list(links)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu",".stat.uci.edu"]
    traps = ["/events", "/event", "/calendar"]
    visited = set()
    try:
        parsed = urlparse(url)

        with open("visited.txt", "r+") as Visit:
            for line in Visit:
                visited.add(line.strip("\n"))
            if url in visited:
                return False
        for d in domains:
            if d in str(parsed.netloc):
                for trap in traps:
                    if trap in parsed.path.lower():
                        return False

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
