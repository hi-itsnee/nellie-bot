import feedparser
import urllib2
from config_helper import get_proxies

def get_rss_items(url):
    proxy=urllib2.ProxyHandler(get_proxies())
    xmldata = feedparser.parse(url, handlers=[proxy])
    return xmldata['entries'] 
