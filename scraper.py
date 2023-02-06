import re
from urllib.parse import urlparse, urldefrag
from collections import defaultdict
from bs4 import BeautifulSoup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    # for link in links:
    #     if(is_valid(link)):
    #         print(link)
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


    stop_words = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    words = []
    filtered = defaultdict(int)
    SubD = defaultdict(int)
    #if word.lower() not in stop_words:
    with open("CommonWords.txt", "r+") as Cw:
        for line in Cw:
            word = line.split(",")
            filtered[word[0]] = int(word[1])

    
    for word in words_re.findall(soup.get_text()):
        if word.lower() not in stop_words:
            filtered[word.lower()] += 1
        words.append(word)

    sorted_items = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    
    with open("CommonWords.txt", "w+") as Common:

        for i in range(len(sorted_items)):
            Common.write(sorted_items[i][0])
            Common.write(",")
            Common.write(str(sorted_items[i][1]))
            Common.write("\n")
            

    #top 50 wrds in file, put words into dict from file, 
    domain = ""
    count = ""
    with open("Longest.txt", "r") as Long:
        line = Long.readline()
        text = line.split(",")
        domain = text[0]
        count = text[1]

    with open("Longest.txt", "w+") as Long2:
        if len(words) > int(count):
            Long2.write(url)
            Long2.write(",")
            Long2.write(str(len(words)))
        else:
            Long2.write(domain)
            Long2.write(",")
            Long2.write(count)
    
    with open("Visited.txt", "a+") as Visit:
        Visit.write(url)
        Visit.write("\n")


    with open("Subdomains.txt", "r") as Dom:
        for line in Dom:
            word = line.split(",")
            SubD[word[0]] = int(word[1])

    parsed = urlparse(url)
    dom = parsed.scheme + "://" + parsed.netloc
    SubD[dom] += 1
    sortedSubD = sorted(SubD.items(), key=lambda x: (x[1],x[0]),  reverse=True)

    with open("Subdomains.txt", "w+") as Sub:
        for i in range(len(sortedSubD)):
            Sub.write(sortedSubD[i][0])
            Sub.write(",")
            Sub.write(str(sortedSubD[i][1]))
            Sub.write("\n")

    for link in soup.find_all('a'):
        #print(urldefrag(link.get('href'))[0])
        links.add(urldefrag(link.get('href'))[0])

    return list(links)

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    domains = [".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu",".stat.uci.edu"]
    traps = ["/events", "/event", "/calendar", "/pdf"]
    visited = set()
    try:
        parsed = urlparse(url)

        with open("Visited.txt", "r+") as Visit:
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
