from config_helper import *
from printing_helper import *
from rest import get

def build_url(keyword):
    url = "http://api.washingtonpost.com/trove/v1/search?q=[KEYWORD]&date=[TODAY]&key=[MYKEY]"
    url = url.replace('[KEYWORD]', keyword)
    url = url.replace('[TODAY]', todays_date_iso())
    url = url.replace('[MYKEY]', get_api_item('washpost','key'))
    return url

def get_stories(keyword):
    hits = {}
    url = build_url(keyword)
    stories = get(url)['itemCollection']['items']
    for story in stories:
        hits[story['displayName']] = story['url']
    return hits
    
def main():
    term = raw_input('What are you searching for: ')
    print_title_link_pairs(get_stories(term)) 

if __name__=="__main__":
    main()
