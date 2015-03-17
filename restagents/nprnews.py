import sys, rest
from config_helper import *
from printing_helper import *

baseurl = "http://api.npr.org/query?date=[TODAY]&searchTerm=[SEARCHTERM]&searchType=mainText&dateType=story&output=JSON&apiKey=[MYKEY]"

def get_stories(term):
    url = baseurl.replace("[TODAY]", todays_date_iso())
    url = url.replace("[MYKEY]", api_info('npr')['key'])
    url = url.replace("[SEARCHTERM]", term)
    data = rest.get(url)
    hits = {}
    if 'message' in data.keys():
        hits[data['message'][0]['text']['$text']] = 'http://www.npr.org'
        return hits
    stories = data['list']['story']
    for story in stories:
        hits[story['title']['$text']] = story['link'][0]['$text']
    return hits

def main():
    term = raw_input("What are you searching for:\t")
    print_title_link_pairs(get_stories(term))

if __name__=="__main__":
    main()
