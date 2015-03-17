from ConfigParser import ConfigParser

def get_cfg():
    cfg = ConfigParser()
    cfg.read('configuration.ini')
    return cfg

def api_info(a):
    cfg = get_cfg()
    items = dict(cfg.items(a))
    return items

def get_api_item(a,b):
    cfg = get_cfg()
    item = cfg.get(a,b)
    return item

def get_proxies():
    cfg = get_cfg()
    proxies = dict(cfg.items('proxy'))
    if len(proxies.keys())==0:
        return None
    first = proxies.keys()[0]
    if proxies[first] == "none":
        return None
    return proxies
