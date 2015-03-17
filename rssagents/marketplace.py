from rss import get_rss_items
from printing_helper import *

def get_stories():
    url = "http://www.marketplace.org/latest-stories/long-feed.xml"
    stories = get_rss_items(url)
    hits = {}
    for story in stories:
        hits[story['title']]=story['link']
    return hits

def main():
    print_title_link_pairs(get_stories())

if __name__=="__main__":
    main()

