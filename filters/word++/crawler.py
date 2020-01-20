import hashlib
import os
import os.path
import re
import urllib.parse
import urllib.request
import urllib.robotparser

from bs4 import BeautifulSoup


class Crawler:
    """Crawls webpages and saves them

    Downloads webpages to disk and recursively visits outlinks.
    """

    def __init__(self, save_dir, net_locs=[], paths=[], sleep_duration=5):
        """
        Args:
            save_dir: directory to save webpages
            net_locs: list of net locations to limit crawling to.
                An empty net_locs indicates all net locations should be visited.
            paths: list of paths to limit crawling to.
                An empty paths indicates all paths should be visited.
            sleep_duration: The duration to sleep between webpage visits
        """
        self.save_dir = save_dir
        self.net_locs = net_locs
        self.paths = paths
        self.sleep_duration = sleep_duration
        self.visited = set()

    def crawl(self, seeds, robots=None):
        """Crawl webpages starting from from seed urls

        Visits webpages starting from seed urls then recursively crawls all urls
        linked from that page.

        Args:
            seeds: seed urls to start crawling from
            robots: url of a robots file
        """
        queue = list(seeds)

        if robots is not None:
            robot = urllib.robotparser.RobotFileParser(robots)
            robot.read()

        while queue:
            url = queue.pop(0)
            if url in self.visited:
                continue
            print(f'Processing {url}')
            
            try:
                contents = self.visit(url)
            except:
                print(f'Error visiting {url}')
                continue

            if contents is None:
                print(contents)
                continue

            self.save_webpage(url, contents)
            soup = BeautifulSoup(contents, 'html.parser')

            links = (link.get('href') for link in soup.find_all('a'))
            for link in links:
                if link is None:
                    continue

                try:
                    new_url = urllib.parse.urljoin(url, link)
                    parsed = urllib.parse.urlparse(new_url)
                    # throw away fragment
                    parsed = _strip_fragment(parsed)
                    new_url = urllib.parse.urlunparse(parsed)
                except:
                    print(f'Error parsing {link}')
                    continue
                    
                if robots is not None and not robot.can_fetch('word++', new_url):
                    # Skip urls prohibited by site's robots file
                    continue

                elif self.net_locs and parsed[1] not in self.net_locs:
                    # Skip urls on disallowed network locations
                    continue

                elif not self._check_path(parsed[2]):
                    continue

                elif new_url in self.visited:
                    # Skip already visited urls
                    continue

                elif parsed[0] != 'http':
                    # Skip non http links
                    continue

                queue.append(urllib.parse.urlunparse(parsed))

    def visit(self, url):
        """Visit a webpage

        Visits a webpage, marks it as visited, and returns its contents

        Args:
            url: url of the webpage
        """
        self.visited.add(url)
        try:
            response = urllib.request.urlopen(url)
            if response.info().get_content_subtype() != 'html':
                # Skip non html resources
                return
        except:
            return

        # in case of redirect
        url = response.url
        self.visited.add(url)

        return response.read()

    def save_webpage(self, url, contents):
        """Saves a webpage using a hash as the filename

        Args:
            url: the webpage's url
            contents: the contents of the webpage
        """
        print(f'Saving {url}')
        (_, _, path, _, _, _) = urllib.parse.urlparse(url)

        save_path = os.path.join(self.save_dir, path[1:])
        os.makedirs(save_path, exist_ok=True)
        file_name = hashlib.sha256(url.encode('utf-8')).hexdigest()

        with open(os.path.join(save_path, file_name), 'wb') as fil:
            fil.write(f'<!-- {url} -->\n'.encode('utf-8'))
            fil.write(contents)


    def _check_path(self, path):
        """Checks if a path is valid
        
        Checks if the path on the webpage should be crawled
        Args:
            path: the path to check
        """
        if not self.paths:
            return True

        for pattern in self.paths:
            if re.fullmatch(pattern, path):
                print(path, pattern, True)
                return True
        print(path, False)
        return False
    
def _strip_fragment(parse_result):
    return parse_result[0], parse_result[1], parse_result[2], parse_result[3], parse_result[4], ''
