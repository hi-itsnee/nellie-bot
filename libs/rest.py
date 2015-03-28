import requests,sys
from config_helper import get_proxies

def get_pem():
    if get_proxies()==None:
        return None
    pem_resp = requests.get('http://curl.haxx.se/ca/cacert.pem', proxies=get_proxies())
    if pem_resp.status_code != 200:
        print "ERROR: Received bad response from api: %d" % pem_resp.status_code
        print "API Message: "+pem_resp.text
        sys.exit()
    f = open('..\pemfile.pem','w')
    f.write(pem_resp.text.encode('utf-8'))
    f.close()
    return '..\pemfile.pem'

def get(url, proxies=None, auth=None,verify = True):
    resp = requests.get(url, proxies=get_proxies(), auth=auth, verify=verify)
    if resp.status_code != 200:
        print "ERROR: Received bad response from api: %d" % resp.status_code
        print "API Message: "+resp.text
        sys.exit()
    return resp.json()
