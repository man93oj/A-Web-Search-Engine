import pickle
from copy import deepcopy

class CalculatePageRank:
    def __init__(self):
        self.pagesCount = 6000
        with open("./CrawledData/crawledLinks_"+str(self.pagesCount),"rb") as data_file:
            self.webLinks = pickle.load(data_file)
            self.reverseWebLinks = pickle.load(data_file)

        with open("./CrawledData/index_"+str(self.pagesCount),"rb") as data_file:
            self.nodes_inlink = pickle.load(data_file)
            self.nodes_outlink = pickle.load(data_file)
            self.inv_index = pickle.load(data_file)
            self.IDF = pickle.load(data_file)

        self.nodes_score = {}
        self.dampFactor = 0.85
        self.nodeCount = len(self.webLinks.keys())

    def start(self):
        init_score = 1/self.nodeCount
        for index,value in self.webLinks.items():
            self.nodes_score[index] = init_score

        nodes_no_outlinks = []
        for index,value in self.nodes_outlink.items():
            if(value == {}):
                nodes_no_outlinks.append(index)

        temp_score = deepcopy(self.nodes_score)
        iterations = 30
        for i in range(iterations):
            self.validate()
            dp = 0
            for node in nodes_no_outlinks:
                dp += (0.85 * (self.nodes_score[node]/self.nodeCount))
            for index in self.webLinks.keys():
                temp_score[index] = (self.dampFactor * self.formula(index)) + ((1-self.dampFactor)/self.nodeCount) + dp
            self.nodes_score = deepcopy(temp_score)


    def formula(self, curNode):
        score = 0
        for neighbour,value in self.nodes_inlink[curNode].items():
            numerator = self.nodes_score[neighbour]
            denominator = self.nodes_outlink[neighbour].keys()
            denominator = len(denominator)
            score += (numerator/denominator)
        return score

    def validate(self):
        sum = 0
        for index,value in self.nodes_score.items():
            sum = sum + (value)

def main():
    PageRankInit = CalculatePageRank()
    PageRankInit.start()

    page_rank = {}
    page_order = sorted(PageRankInit.nodes_score.items(), key=lambda kv: kv[1], reverse=True)

    rank = 1
    for page in page_order:
        page_rank[page[0]] = rank
        rank = rank + 1
    with open("./CrawledData/pagerank_"+str(PageRankInit.pagesCount),"wb") as outfile:
        pickle.dump(page_rank, outfile)

    print("Terminating PageRank program")

if(__name__=="__main__"):
    main()
