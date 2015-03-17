from rss import get_rss_items
from printing_helper import *

def get_stories(title):
    url = "http://www.buzzfeed.com/[TITLE].xml"
    if (title=='homepage'):
        title = 'index'
    url = url.replace("[TITLE]", title)
    stories = get_rss_items(url)
    hits = {}
    for story in stories:
        hits[story['title']]=story['link']
    return hits

def main():
    categories = ['homepage', 'usnews', 'animals', 'tech', 'entertainment', 'sports']
    i = 1
    for category in categories:
        print "%d: %s" % (i, category)
        i += 1
    n=int(raw_input("Enter choice of feed:\t"))
    url = "http://www.buzzfeed.com/[TITLE].xml"
    print_title_link_pairs(get_stories(categories[n-1]))

if __name__=="__main__":
    main()
