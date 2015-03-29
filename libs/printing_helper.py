from datetime import date
import sys
import urllib2
from config_helper import get_proxies

def print_html_pairs(adict):
    titles = adict.keys()
    html_render = "<!doctype html><title>results</title>"
    for title in titles:
        try:
            html_render += title+"&nbsp;&nbsp;"+adict[title]
        except UnicodeEncodeError:
            print "Skipping"
        html_render +="<p>"
    return html_render

def print_title_link_pairs(adict):
    titles = adict.keys()
    for title in titles:
        try:
            print title
            print adict[title]
            print "-------------------------------------"
        except UnicodeEncodeError:
            print "Skipping"

def todays_date_iso():
    return str(date.isoformat(date.today()))

def get_placekitten():
    proxy = urllib2.ProxyHandler(get_proxies())
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    kittens = urllib2.urlopen('http://placekitten.com')
    response = kittens.read()
    body = response[559:1000]
    return body
