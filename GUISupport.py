import easygui as eg

def get_input(msg, title):
    text = eg.enterbox(msg, title)
    if text is None:
        exit()
    return text

def display_results (webLinks, page_order, PreprocessedQuery):
    msg = "Preprocessed query: "+str(PreprocessedQuery)+"\nThese are the results of your query, you can double click" \
                                                   " or select and press ok on a" \
                                                   " result to open the web page in a new tab of your default browser." \
                                                   " Press cancel to go back to the main menu."
    results = []
    for i in range(0, 10):
        results.append(webLinks[page_order[i][0]])

    return eg.choicebox(msg, "SearchEngine results", results)
