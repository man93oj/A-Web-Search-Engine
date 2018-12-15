import requests, nltk, re, pickle

from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import deque
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from copy import deepcopy
from urllib.parse import urlparse

class PreProcessor:

    def __init__(self):
        self.pagesCount = 6000

        with open("./CrawledData/crawledData_"+str(self.pagesCount),"rb") as data_file:
            self.webLinks = pickle.load(data_file)
            self.reverseWebLinks = pickle.load(data_file)

        self.nodes_inlink = dict()
        self.nodes_outlink = dict()

        for index in self.webLinks.keys():
            self.nodes_inlink[index] = {}
            self.nodes_outlink[index] = {}

        self.inv_index = {}
        self.IDF = {}
        self.stream_length = {}

        self.inv_index_title = {}
        self.IDF_title = {}
        self.stream_length_title = {}

        self.url_split = {}
        self.no_slashes = {}
        self.len_URL = {}

        self.ps = PorterStemmer()
        self.nodes_score = dict()
        self.nodes = dict()
        self.regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))

    def tag_visible(self,element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    def text_from_html(self,body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)

    def start(self):

        for index,value in self.webLinks.items():
            with open("./CrawledData/"+str(index),"r") as file:
                self.inv_index[index] = {}
                self.inv_index_title[index] = {}

                temp_word_list = []
                r = file.read()

                words = self.text_from_html(r)
                words = " ".join(re.findall("[a-zA-Z0-9]+", words))
                words = words.split(" ")
                self.stream_length[index] = len(words)
                for word in words:
                    if(word not in self.stop_words):
                        word = word.lstrip(" ")
                        word = word.rstrip(" ")
                        word = word.lower()
                        word = self.ps.stem(word)

                        self.inv_index[index][word] = self.inv_index[index].get(word,0) + 1
                        if(word not in temp_word_list):
                            self.IDF[word] = self.IDF.get(word,0) + 1
                        temp_word_list.append(word)

                temp_word_list = []
                soup = BeautifulSoup(r, 'lxml')
                try:
                    tags = soup.find('title').text
                    words = tags.split(" ")
                    self.stream_length_title[index] = len(words)

                    for word in words:
                        if(word not in self.stop_words):
                            word = word.lstrip(" ")
                            word = word.rstrip(" ")
                            word = word.lower()
                            word = self.ps.stem(word)

                            self.inv_index_title[index][word] = self.inv_index_title[index].get(word,0) + 1
                            if(word not in temp_word_list):
                                self.IDF_title[word] = self.IDF_title.get(word,0) + 1
                            temp_word_list.append(word)
                except:
                    pass

                temp_word_list = []
                split_dot = self.webLinks[index].split(".")
                self.url_split[index] = {}
                for element in split_dot:
                    element = " ".join(re.findall("[a-zA-Z0-9]+", element)) #Only alphabets and numbers
                    element = element.split(" ")
                    element_new = ""
                    for x in element:
                        element_new += self.ps.stem(x)
                        self.url_split[index][element_new] = self.url_split[index].get(element_new,0) + 1
                self.len_URL[index] = len(value)
                self.no_slashes[index] = value.count("/")


                soup = BeautifulSoup(r, 'lxml')
                tags = soup.find_all('a')
                for tag in tags:
                    try:
                        if(re.match(self.regex, tag["href"]) is not None):
                            o = urlparse(tag["href"])
                            temp_href = ((o.netloc+o.path).lstrip("www.").rstrip("/"))
                            if(temp_href in self.webLinks.values()):

                                temp_val = self.reverseWebLinks[temp_href]
                                self.nodes_outlink[index][temp_val] = self.nodes_outlink[index].get(temp_val,0) + 1
                                self.nodes_inlink[temp_val][index] = self.nodes_inlink[temp_val].get(index,0) + 1
                    except:
                        continue

        with open("./CrawledData/index_"+str(self.pagesCount),"wb") as outfile:
            pickle.dump(self.nodes_inlink, outfile)
            pickle.dump(self.nodes_outlink,outfile)
            pickle.dump(self.inv_index,outfile)
            pickle.dump(self.IDF,outfile)

        outlink_count = {}
        inlink_count = {}
        for k,v in self.nodes_outlink.items():
            outlink_count[k] = len(v)
        for k,v in self.nodes_inlink.items():
            inlink_count[k] = len(v)

        for k,v in self.IDF.items():
            self.IDF[k] = 1/v

        for k,v in self.IDF_title.items():
            self.IDF_title[k] = 1/v


        self.TF_IDF_title = deepcopy(self.inv_index_title)
        for k,v in self.inv_index_title.items():
            for k1,v1 in v.items():
                self.TF_IDF_title[k][k1] = v1*self.IDF_title[k1]
        self.TF_IDF = deepcopy(self.inv_index)
        for k,v in self.inv_index.items():
            for k1,v1 in v.items():
                self.TF_IDF[k][k1] = v1*self.IDF[k1]

        with open("./CrawledData/index2_"+str(self.pagesCount),"wb") as outfile:
            pickle.dump(self.stream_length_title, outfile)
            pickle.dump(self.stream_length, outfile)
            pickle.dump(self.IDF_title, outfile)
            pickle.dump(self.IDF,outfile)
            pickle.dump(self.inv_index_title, outfile)
            pickle.dump(self.inv_index,outfile)
            pickle.dump(self.TF_IDF_title,outfile)
            pickle.dump(self.TF_IDF,outfile)
            pickle.dump(self.no_slashes, outfile)
            pickle.dump(self.len_URL, outfile)
            pickle.dump(outlink_count, outfile)
            pickle.dump(inlink_count, outfile)
            pickle.dump(self.url_split, outfile)

def main():
    PreProcessorInit = PreProcessor()
    PreProcessorInit.start()
    print("PreProcessoring Completed!")

if(__name__=="__main__"):
    main()
