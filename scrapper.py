import urllib2
import bs4 #beautiful soup


# Downloads the html and scrapes a list of links
def scrapeLinks(pageUrl):
    links  = []

    for page in range(10):
        url = pageUrl + "/" + page + "/"

        #open and create a soup
        source = urllib2.urlopen(pageUrl).read()
        pageSoup = bs4.BeautifulSoup(source,'html.parser')
        

        #Extract Title and content
        articles = pageSoup.find('div',{'id':'main'}).findAll('article')
        
        for article in articles:
            title = article.find('h3').a.contents[0]
            url = article.find('h3').a["href"]
            links.append({
                "title" : title,
                "url": url
            })
            
        print "- scrapped %i links" %len(links)
    return links

# extract data from raw article
def extract_data(pageSoup):
    data = {}
    raw_article = pageSoup.find("article")
    
    data["id"] = raw_article["id"]
    data["date"] = raw_article.find("header").p.span.contents[0]
    data["title"] = raw_article.find("header").h1.contents[0]
    #content
    data["content"] = raw_article.find("div",{'class': 'article-post-content'})
    #tags
    tags = raw_article.find("aside",{'class': 'tags'}).findAll("a")
    data["tags"] = [ x.contents[0] for x in tags]

    return data

# using a list of links it scrapes articles and returns data
def scrape_articles(links):
    data  = []
    for link in links:
        article_url = link["url"]
        source = urllib2.urlopen(article_url).read()
        pageSoup = bs4.BeautifulSoup(source,'html.parser')
        #extract raw features 
        article_data = extract_data(pageSoup) 
        data.append( article_data )
    return data

#
url = "http://www.latribuna.hn/tag/crimenes-en-honduras/page/"
links = scrapeLinks(url)
articles = scrape_articles(links)

for article in articles:
    print article["title"]



