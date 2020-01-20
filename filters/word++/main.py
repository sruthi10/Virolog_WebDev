from crawler import Crawler

ROBOTS_URL = "http://journals.plos.org/robots.txt"
WEBPAGE_SAVE_LOCATION = "webpages/"


def main():
    crawler = Crawler(WEBPAGE_SAVE_LOCATION,
                      net_locs = ['journals.plos.org'],
                      paths = ['/plosbiology/volume', '/plosbiology/issue', '/plosbiology/article'])
    crawler.crawl(['http://journals.plos.org/plosbiology/volume'], ROBOTS_URL)


if __name__ == '__main__':
    main()
