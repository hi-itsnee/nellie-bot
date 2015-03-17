import requests,sys
from config_helper import get_proxies

def get(url, proxies=None, auth=None):
    resp = requests.get(url, proxies=get_proxies(), auth=auth)
    if resp.status_code != 200:
        print "ERROR: Received bad response from api: %d" % resp.status_code
        print "API Message: "+resp.text
        sys.exit()
    return resp.json()
