import time, re, os, pickle, requests

import GUISupport as ui
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import deque

class Crawler:

    def __init__(self):

        # MainUrl = ui.get_input("Please enter the Url to Parse from: ", "WebCrawler")
        # self.pagesCount = int (ui.get_input("Please give me the page threshold Value: ", "WebCrawler"))

        self.pagesCount = 6000
        MainUrl = "https://www.cs.uic.edu/"

        self.pageNo = 0
        self.urlQueue = deque()
        self.webLinks = {}
        self.reverseWebLinks = {}

        self.include_content = "uic.edu"
        self.regexp = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        self.exclude_content = ['mailto:', 'favicon', '.ico', '.css', '.js',
                                '.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc',
                                '.JPG', '.mp4', '.svg']

        o = urlparse(MainUrl)
        self.urlQueue.append((o.netloc+o.path).lstrip("www.").rstrip("/"))

    def crawl(self):
        while(len(self.urlQueue) != 0):
            try:
                Url = self.urlQueue.popleft()
                r = requests.get("http://"+Url)
                if(r.status_code == 200):
                    self.webLinks[self.pageNo] = Url
                    filename = "./CrawledData/"+str(self.pageNo)
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with open(filename, "w") as f:
                        f.write(r.text)

                    soup = BeautifulSoup(r.text, 'lxml')
                    tags = soup.find_all('a')
                    for tag in tags:
                        try: #make sure there is a href tag. For <a class="", this will throw error. Hence, the try catch
                            if(re.match(self.regexp, tag["href"]) is not None and not any(word in tag["href"] for word in self.exclude_content)):
                                o = urlparse(tag["href"])
                                temp_href = ((o.netloc+o.path).lstrip("www.").rstrip("/"))
                                if(self.include_content in tag["href"] and temp_href not in self.webLinks.values() and temp_href not in self.urlQueue):
                                    self.urlQueue.append(temp_href)
                        except:
                            continue

                    self.reverseWebLinks = {v: k for k, v in self.webLinks.items()}
                    if(len(self.webLinks) > self.pagesCount):
                        with open("./CrawledData/crawledLinks_"+str(self.pagesCount),"wb") as outfile:
                            pickle.dump(self.webLinks,outfile)
                            pickle.dump(self.reverseWebLinks,outfile)
                        break

                    self.pageNo += 1
            except Exception as e:
                print(e)
                print("Connection failed for ", Url)
                time.sleep(5)
                continue

def main():
    WebCrawlerInit = Crawler()
    WebCrawlerInit.crawl()
    print("WebCrawlering finished")

if(__name__=="__main__"):
    main()
