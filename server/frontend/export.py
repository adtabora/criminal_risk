import pandas as pd
import numpy as np
import json

from flask.db import DB



#Exports to csv in a format to train by category (without NE tags)
def exportCategory():
    db = DB()
    # get all of the tagged articles
    filters = [("REVIEWED","=",1)]
    articles = db.getArticles(filters, columns=["ID", "CATEGORY"] )
    db.close()


    found_size = len(articles)

    indices = [art[0] for art in articles]

    # get the original title and content
    base_df = pd.read_csv("./files/articles.csv")  
    base_df = base_df.loc[indices]

    print " ---- "
    print found_size
    print base_df.shape

    data = []
    index = 0
    for art_index, article in base_df.iterrows():
        
        raw_text = article["content"]
        raw_title = unicode(article["title"],"utf8")
        soup = bs4.BeautifulSoup(raw_text, 'html.parser')
        text = soup.get_text().replace("\n","")

        #add a row 
        data.append( [art_index, raw_title, text, articles[index][1]] )
        index += 1

    articles_df = pd.DataFrame(data,columns=["id","title","content","category"])

    articles_df.to_csv("./files/documents.csv",index=False, encoding='utf-8')

def exportTags():
    db = DB()
    # get all of the tagged articles that are category criminal
    filters = [("REVIEWED","=",1), ("CATEGORY", "=", "Criminal")]
    articles = db.getArticles(filters, columns=["ID","TITLE","SENTENCES"] )
    db.close()
    #for convinience create a DataFrame
    print len(articles)
    df = pd.DataFrame(articles,columns=["article_id","title","content"])
    print df.shape

    #convert title and content strings into a json
    df.loc[:,"title"] = df.title.apply(lambda x: json.loads(x) )
    df.loc[:,"content"] = df.content.apply(lambda x: json.loads(x) )


    df.to_csv("./files/criminal_articles.csv",index=False)




# exportCategory()    
exportTags()