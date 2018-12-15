import numpy as np
import pickle
from copy import deepcopy
import operator
from nltk.stem import PorterStemmer
import GUISupport as ui
import webbrowser

def ShowResults(webLinks, page_order, query):
    choice = ui.display_results(webLinks, page_order, query)
    if choice is None:
        exit()
    else:
        open_website(choice)

def open_website(url):
    webbrowser.open("http://"+url+"/", new=2, autoraise=True)

if (__name__ == "__main__"):

    pagesCount = 6000
    query = ui.get_input("Search Query: ", "SearchEngine")
    query = query.split(" ")
    temp_q = ""
    ps = PorterStemmer()
    for word in query:
        temp = word.lower()
        temp = ps.stem(temp)
        temp_q += (temp + " ")

    query = temp_q.rstrip(" ")

    with open("./.CrawledData/crawledLinks_"+str(pagesCount),"rb") as data_file:
        webLinks = pickle.load(data_file)

    with open("./.CrawledData/index2_"+str(pagesCount),"rb") as outfile:
        stream_length_title = pickle.load(outfile)
        stream_length = pickle.load(outfile)
        IDF_title = pickle.load(outfile)
        IDF = pickle.load(outfile)
        inv_index_title = pickle.load(outfile)
        inv_index = pickle.load(outfile)
        TF_IDF_title = pickle.load(outfile)
        TF_IDF = pickle.load(outfile)
        no_slashes = pickle.load(outfile)
        len_URL = pickle.load(outfile)
        outlink_count = pickle.load(outfile)
        inlink_count = pickle.load(outfile)
        url_split = pickle.load(outfile)

    with open("./.CrawledData/pagerank_"+str(pagesCount),"rb") as outfile:
        page_rank = pickle.load(outfile)

    IDF_q = 0
    IDF_q_title = 0
    for word in query:
        IDF_q += IDF.get(word, 0)
        IDF_q_title += IDF_title.get(word, 0)

    sum_tf = {}
    min_tf = {}
    max_tf = {}
    mean_tf = {}
    sum_url = {}
    covered_terms = {}

    for doc, word_map in inv_index.items():
        covered_terms[doc] = 0

    temp = query.split(" ")
    for word in temp:
        for doc, word_map in inv_index.items():
            sum_tf[doc] = sum_tf.get(doc, 0) + word_map.get(word, 0)
            if (word_map.get(word, 0) != 0):
                covered_terms[doc] = covered_terms.get(doc) + 1

            if (min_tf.get(doc, 0) == 0):
                min_tf[doc] = word_map.get(word, 0)
            else:
                if (min_tf[doc] > word_map.get(word, float("Inf"))):
                    min_tf[doc] = word_map.get(word)

            if (max_tf.get(doc, 0) == 0):
                max_tf[doc] = word_map.get(word, 0)
            else:
                if (max_tf[doc] < word_map.get(word, 0)):
                    max_tf[doc] = word_map.get(word, 0)

    mean_tf = deepcopy(sum_tf)
    for doc, tf in mean_tf.items():
        if (covered_terms[doc] != 0):
            mean_tf[doc] /= covered_terms[doc]
        else:
            mean_tf[doc] = 0

    covered_term_ratio = {}
    for doc, freq in covered_terms.items():
        covered_term_ratio[doc] = freq / len(temp)

    sum_tf_title = {}
    min_tf_title = {}
    max_tf_title = {}
    mean_tf_title = {}
    covered_terms_title = {}

    temp = query.split(" ")
    for doc, word_map in inv_index_title.items():
        covered_terms_title[doc] = 0
    for word in temp:
        for doc, word_map in inv_index_title.items():
            sum_tf_title[doc] = sum_tf_title.get(doc, 0) + word_map.get(word, 0)
            if (word_map.get(word, 0) != 0):
                covered_terms_title[doc] = covered_terms_title.get(doc) + 1

            if (min_tf_title.get(doc, 0) == 0):
                min_tf_title[doc] = word_map.get(word, 0)
            else:
                if (min_tf_title[doc] > word_map.get(word, float("Inf"))):
                    min_tf_title[doc] = word_map.get(word)

            if (max_tf_title.get(doc, 0) == 0):
                max_tf_title[doc] = word_map.get(word, 0)
            else:
                if (max_tf_title[doc] < word_map.get(word, 0)):
                    max_tf_title[doc] = word_map.get(word, 0)

    mean_tf_title = deepcopy(sum_tf_title)
    for doc, tf in mean_tf_title.items():
        if (covered_terms_title[doc] != 0):
            mean_tf_title[doc] /= covered_terms_title[doc]
        else:
            mean_tf_title[doc] = 0

    covered_term_ratio_title = {}
    for doc, freq in covered_terms_title.items():
        covered_term_ratio_title[doc] = freq / len(temp)

    sum_tf_idf_title = {}
    min_tf_idf_title = {}
    max_tf_idf_title = {}
    mean_tf_idf_title = {}
    for word in temp:
        for doc, word_map in TF_IDF_title.items():
            sum_tf_idf_title[doc] = sum_tf_idf_title.get(doc, 0) + word_map.get(word, 0)

            if (min_tf_idf_title.get(doc, 0) == 0):
                min_tf_idf_title[doc] = word_map.get(word, 0)
            else:
                if (min_tf_idf_title[doc] > word_map.get(word, float("Inf"))):
                    min_tf_idf_title[doc] = word_map.get(word)

            if (max_tf_idf_title.get(doc, 0) == 0):
                max_tf_idf_title[doc] = word_map.get(word, 0)
            else:
                if (max_tf_idf_title[doc] < word_map.get(word, 0)):
                    max_tf_idf_title[doc] = word_map.get(word, 0)

    mean_tf_idf_title = deepcopy(sum_tf_idf_title)
    for doc, tf in mean_tf_idf_title.items():
        if (covered_terms_title[doc] != 0):
            mean_tf_idf_title[doc] /= covered_terms_title[doc]
        else:
            mean_tf_idf_title[doc] = 0

    sum_tf_idf = {}
    min_tf_idf = {}
    max_tf_idf = {}
    mean_tf_idf = {}
    for word in temp:
        for doc, word_map in TF_IDF.items():
            sum_tf_idf[doc] = sum_tf_idf.get(doc, 0) + word_map.get(word, 0)

            if (min_tf_idf.get(doc, 0) == 0):
                min_tf_idf[doc] = word_map.get(word, 0)
            else:
                if (min_tf_idf[doc] > word_map.get(word, float("Inf"))):
                    min_tf_idf[doc] = word_map.get(word)

            if (max_tf_idf.get(doc, 0) == 0):
                max_tf_idf[doc] = word_map.get(word, 0)
            else:
                if (max_tf_idf[doc] < word_map.get(word, 0)):
                    max_tf_idf[doc] = word_map.get(word, 0)

    mean_tf_idf = deepcopy(sum_tf_idf)
    for doc, tf in mean_tf_idf.items():
        if (covered_terms[doc] != 0):
            mean_tf_idf[doc] /= covered_terms[doc]
        else:
            mean_tf_idf[doc] = 0


    rank = {}

    for word in temp:
        for doc, word_map in url_split.items():
            sum_url[doc] = sum_url.get(doc, 0) + word_map.get(word, 0)

    max_inlink = max(inlink_count.items(), key=operator.itemgetter(1))[1]

    for doc in inv_index.keys():
        ip = []
        ip.append(40*covered_terms_title[doc])
        ip.append(100*covered_terms[doc])

        ip.append(40*covered_term_ratio_title[doc])
        ip.append(100*covered_term_ratio[doc])
        try:
            ip.append(0.0001*stream_length_title[doc])
        except:
            ip.append(0)
        ip.append(0*stream_length[doc])

        ip.append(0.01*IDF_q_title)
        ip.append(0.01*IDF_q)

        ip.append(1*sum_tf_title[doc])
        ip.append(0.001*sum_tf[doc])

        ip.append(0.01*min_tf_title[doc])
        ip.append(0.01*min_tf[doc])

        ip.append(0.01*max_tf_title[doc])
        ip.append(0.01*max_tf[doc])

        ip.append(0.01*mean_tf_title[doc])
        ip.append(0.01*mean_tf[doc])

        ip.append(0.001*sum_tf_idf_title[doc])
        ip.append(0.001*sum_tf_idf[doc])

        ip.append(0.01*min_tf_idf_title[doc])
        ip.append(0.01*min_tf_idf[doc])

        ip.append(0.01*max_tf_idf_title[doc])
        ip.append(0.01*max_tf_idf[doc])

        ip.append(0.01*mean_tf_idf_title[doc])
        ip.append(0.01*mean_tf_idf[doc])

        ip.append(-1*2*no_slashes[doc])
        ip.append(-1*1*len_URL[doc])

        ip.append((inlink_count[doc]/max_inlink)*110)
        ip.append(0.00001*outlink_count[doc])

        ip = sum(ip)

        rank[doc] = ip

    ITpage_order = sorted(rank.items(), key=lambda kv: kv[1], reverse=True)

    # With Out intelligent component
    for doc in inv_index.keys():
        ip = []
        ip.append(40*covered_terms_title[doc])
        ip = sum(ip)
        rank[doc] = ip

    WOITpage_order = sorted(rank.items(), key=lambda kv: kv[1], reverse=True)
    msg = "!!RESULTS ARE CALCULATED!! \n" \
          "Please enter '1' to see the results with Intelligent Component \n" \
          "or '0' to see the results with out Intelligent Component \n" \
          " Press cancel to close the popup"

    i = ui.get_input(msg, "SearchEngine")
    if (i == '1'):
        ShowResults(webLinks, ITpage_order, query)
    elif (i == '0'):
        ShowResults(webLinks, WOITpage_order, query)
