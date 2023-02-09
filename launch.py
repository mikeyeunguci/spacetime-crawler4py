from configparser import ConfigParser
from argparse import ArgumentParser

from utils.server_registration import get_cache_server
from utils.config import Config
from crawler import Crawler
import os


def main(config_file, restart):
    #Creates files before running scraper.py
    if not os.path.exists("Visited.txt"):
        f = open("Visited.txt", "w")
        f.close()
    if not os.path.exists("CommonWords.txt"):
        l = open("CommonWords.txt", "w")
        l.close()
    if not os.path.exists("Subdomains.txt"):
        a = open("Subdomains.txt", "w")
        a.close()

    if not os.path.exists("Longest.txt"):
        d = open("Longest.txt", "w")
        d.write("URL, 0")
        d.close()
    cparser = ConfigParser()
    cparser.read(config_file)
    config = Config(cparser)
    config.cache_server = get_cache_server(config, restart) #
    crawler = Crawler(config, restart)
    crawler.start()



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--restart", action="store_true", default=False)
    parser.add_argument("--config_file", type=str, default="config.ini")
    args = parser.parse_args()
    main(args.config_file, args.restart)
