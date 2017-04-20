import urllib2
import bs4 #beautiful soup

from datetime import datetime
import pandas as pd
import numpy as np

def getLinks():
    sitemap_url = "http://www.latribuna.hn/sitemap_index.xml"
    article_urls = []
    article_dates =[]
    date_format = "%Y-%m-%dT%H:%M:%S"


    print "- scrapping main sitemap"
    source = urllib2.urlopen(sitemap_url).read()
    main_sitemap = bs4.BeautifulSoup(source,"lxml")
    sitemap_urls = [loc.contents[0] for loc in  main_sitemap.findAll("loc")]
    
    #just for testing reasons...
    # sitemap_urls = sitemap_urls[1:3]
    print "number of sitemaps: %i" %len(sitemap_urls)
    
    print "- scrapping sitemaps"
    counter = 0
    for url in sitemap_urls:
        counter += 1
        print "- sitemap %i of %i"%(  counter ,len(sitemap_urls))
        sitemap_source = urllib2.urlopen(url).read()
        sitemap = bs4.BeautifulSoup(sitemap_source,"lxml")
        article_urls = article_urls + [loc.contents[0] for loc in  sitemap.findAll("loc")]
        article_dates = article_dates + [datetime.strptime(lastmod.contents[0][:-6],date_format) \
                                         for lastmod in  sitemap.findAll("lastmod")]
        
    print "number of articles extracted: %i" %len(article_urls)
    
    print "- save links to file"
    links_df = pd.DataFrame({
            "url": article_urls,
            "date": article_dates
        })
    links_df.to_csv("./files/links.csv")
     
    print "- Done."