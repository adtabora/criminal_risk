import urllib2
import bs4 #beautiful soup

import random
import time
import pandas as pd

# using a list of links it scrapes articles and returns data
def scrape(url):
    print url
    # read and parse the page
    source = urllib2.urlopen(url).read()
    pageSoup = bs4.BeautifulSoup(source,'html.parser')
    
    #extract raw features 
    data = {}
    raw_article = pageSoup.find("article")
    #basic data
    data["id"] = raw_article["id"]
    data["date"] = raw_article.find("header").p.span.contents[0]
    data["title"] = raw_article.find("header").h1.contents[0]
    #content
    data["content"] = raw_article.find("div",{'class': 'article-post-content'})
    #tags
    tag_container = raw_article.find("aside",{'class': 'tags'})
    if tag_container != None:
        tags = tag_container.findAll("a")
        data["tags"] = [ x.contents[0] for x in tags]
    else:
        data["tags"] = "None"

    return data

# function that scrapes articles from links not yet visited. 
# max_articles: we don't want to overflow the site with traffic, trying to be a good web citizen
def scrape_articles(max_articles = 10):
    # 1. read links.csv and select only those that havent been scraped  
    print "- reading links.csv"
    links_full = pd.read_csv("./files/links.csv")
    links = links_full[links_full["scraped"]==False].head(max_articles)

    # 2. for each link scrape 
    print "- scraping %i links" %links.shape[0]
    data = []
    error_index = []
    counter = 0
    for index, link in links.iterrows():
        counter += 1
        print "- scraping %i of %i" %(counter, links.shape[0])
        try:
            article_data = scrape(link["url"])
            data.append(article_data)
        except Exception, e:
            print "-- ERROR --"
            print e
            error_index.append(e)

    # 3. save data into csv
    print "- saving scraped data"
    #TODO: read from csv and append the new data
    try:
        articles_df = pd.read_csv("./files/articles.csv")
    except Exception, e:
        articles_df = pd.DataFrame({})
    columns = ["id", "date", "title","content", "tags"]
    new_articles = pd.DataFrame(data, columns=columns)
    articles_df = articles_df.append(new_articles)
    articles_df.to_csv("./files/articles.csv",index=False, encoding='utf-8')

    # 4. update links with scraped == True
    print "- updating links.csv"
    links_full.loc[links.index.values,"scraped"] = True
    # handling error
    if len(error_index) > 0:
        links_full.loc[error_index,"scraped"] == False
    links_full.to_csv("./files/links.csv",index=False)

# in order to be a "good web citizen" the scrapper will execute randomly between 10 and 30 seconds
# so that it doesn't generate too much traffic to the website.
for i in range(84):
    print "-- Iteration %i --" %i 
    wait = random.randint(10,30)
    scrape_articles(10)
    print "- wait %i seconds" %i 
    time.sleep(wait)
    

