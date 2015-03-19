import requests, sys
from ConfigParser import ConfigParser
from config_helper import api_info, get_proxies
from printing_helper import *
import rest

def get_top_stories():
    url = "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty"
    return rest.get(url, proxies = get_proxies(), verify=rest.get_pem())

def get_stories(n):
    hn500=get_top_stories()
    hntopn = hn500[:n]
    hits = {}
    baseurl = "https://hacker-news.firebaseio.com/v0/item/[STORY].json?print=pretty"
    for story in hntopn:
        url=baseurl.replace("[STORY]",str(story))
        astory = rest.get(url, get_proxies(), verify=rest.get_pem())
        hits[astory['title']]=astory['url']
        #print "%s:\n%s" % (astory['title'],astory['url'])
    return hits

def main():
    print_title_link_pairs(get_stories(10))

if __name__=="__main__":
    main()
