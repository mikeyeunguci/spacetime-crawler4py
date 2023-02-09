import re
from urllib.parse import urlparse, urldefrag, urljoin
import urllib.robotparser
from utils import download
from collections import defaultdict
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
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

    # Created a set(links) to return extracted links with no duplicates
    # Regular expression is used to catch words in word(list) which is used to find the page with the most words
    # Stopwords is a list of stopwords to skip when reading checking for the most common words
    # Filtered dictionary is used to keep track of the most common words during the crawl
    # SubD is a dictionary used to keep detect the number of unique pages per each subdomain

    links = set()
    words_re = re.compile(r'\b\w+\b')
    stop_words = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    words = []
    filtered = defaultdict(int)
    SubD = defaultdict(int)

    # Checks if page returns a valid status code with no errors, returns empty otherwise
    # Beautiful Soup is used for parsing html documents to extract relevant data, returns empty list if page is empty
    if(resp.status != 200 or resp.error != None):
        return []
    try:
        if str(url).endswith(".xml"):   
            soup = BeautifulSoup(resp.raw_response.content, 'xml')
            for link in soup.find_all("loc"):
                links.add(link.text)
            with open("Visited.txt", "a+") as Visit1:
                Visit1.write(url)
                Visit1.write("\n")
            return list(links)
        else:
            soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    except AttributeError:
        return []



    # Opens CommonWords.txt and adds all words and their frequencies found throughout the crawl into filtered dictionary
    with open("CommonWords.txt", "r+") as Cw:
        for line in Cw:
            word = line.split(",")
            filtered[word[0]] = int(word[1])

    # Puts all words and their frequencies found in url into filtered dictionary while also filtering out stop words
    # Also puts unfiltered words into words(list)
    for word in words_re.findall(soup.get_text()):
        if word.lower() not in stop_words:
            filtered[word.lower()] += 1
        words.append(word)

    # sorts dictionary by frequencies in descending order
    sorted_items = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    
    # Opens CommonWords.txt to rewrite it with current common words with their frequencies
    with open("CommonWords.txt", "w+") as Common:
        for i in range(len(sorted_items)):
            Common.write(sorted_items[i][0])
            Common.write(",")
            Common.write(str(sorted_items[i][1]))
            Common.write("\n")
            

    # domain is the url with the longest page (most words)
    # count is the number of words in a page
    domain = ""
    count = ""

    with open("Longest.txt", "r") as Long:
        line = Long.readline()
        text = line.split(",")
        domain = text[0]
        count = text[1]

    # If the amount of words in current page is greater than what was in longest.txt, then set to current url and current length of words
    # else write back previous domain and count
    with open("Longest.txt", "w+") as Long2:
        if len(words) > int(count):
            Long2.write(url)
            Long2.write(",")
            Long2.write(str(len(words)))
        else:
            Long2.write(domain)
            Long2.write(",")
            Long2.write(count)

    # Add current url to Visited.txt
    with open("Visited.txt", "a+") as Visit:
        Visit.write(url)
        Visit.write("\n")

    # Opens Subdomains and adds all subdomains into SubD dictionary to track the unique pages for each subdomain
    with open("Subdomains.txt", "r") as Dom:
        for line in Dom:
            word = line.split(",")
            SubD[word[0]] = int(word[1])

    # Adds current url to SubD dictionary
    parsed = urlparse(url)
    dom = parsed.scheme + "://" + parsed.netloc
    SubD[dom] += 1

    # Sorts SubD by descending frequency and alphabetically
    sortedSubD = sorted(SubD.items(), key=lambda x: (x[1],x[0]),  reverse=True)

    # Writes sorted subdomains with their frequencies into Subdomains.txt
    with open("Subdomains.txt", "w+") as Sub:
        for i in range(len(sortedSubD)):
            Sub.write(sortedSubD[i][0])
            Sub.write(",")
            Sub.write(str(sortedSubD[i][1]))
            Sub.write("\n")

    # Finds all links in current url and transforms relative links into absolute urls
    # Adds absoulte urls into a set of links which is then returned as a list of links
    
    if not str(url).endswith(".xml"):
        for link in soup.find_all('a'):
            parsed = urlparse(urldefrag(link.get('href'))[0])
            if parsed.netloc == "":
                parsed = urljoin(url, urldefrag(link.get('href'))[0])
                links.add(parsed)
            else:
                links.add(urldefrag(link.get('href'))[0])

    # Adds sitemaps urls from current URL's robots.txt into set list of urls to return as list
    parsed = urlparse(url)

    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
    rp.read()
    sitemap = rp.site_maps()
    if sitemap != None:
        for i in sitemap:
            links.add(i)
    
    
    return list(links)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    # These are the only domains we want to crawl (domains)
    # (traps) Checks relative paths/urls to avoid traps
    # Keeps track of visited urls with a set (visited)
    # If url already in set (visited), returns False
    # Checks robots.txt for paths to not crawl, will return False if path is Disallowed
    domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu",".stat.uci.edu"]                   
    traps = ["/events", "/event", "/calendar", "/pdf"]
    visited = set()
    trapPaths = defaultdict(list)
    parsed = urlparse(url)
    try:

        trap1 = set(str(parsed.path).split('/'))
        for word in trap1:
            if str(parsed.path).split('/').count(word) > 1:
                return False
        try:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
            rp.read()
            
            if not rp.can_fetch("*", url):
                return False
        except:
            return False

        with open("Visited.txt", "r+") as Visit:
            for line in Visit:
                visited.add(line.strip("\n"))
                if str(parsed.path).split('/')[-1] in line and parsed.netloc in line:
                    return False
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
                    + r"|png|tiff?|mid|mp2|mp3|mp4|ppsx"
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
