from datetime import date
import wx,sys
import wx.lib.agw.hyperlink as hl
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

class Results(wx.Frame):
    def __init__(self, parent, id, title, stories):
        wx.Frame.__init__(self, parent, id, title,size=(500,400))
        #self.Bind(wx.EVT_CLOSE, self.OnClose)
        if stories == {}:
            wx.StaticText(self, -1, "Sorry! No items found", (20, 30))
            wx.StaticText(self, -1, get_placekitten(),(20,100))
            wx.Button(self, -1, 'Exit', (240, 370))
            self.Bind(wx.EVT_BUTTON, self.OnClose)
        else:
            self.sw = wx.ScrolledWindow(self)
            panel = wx.Panel(self.sw)
            titles=stories.keys()
            start=0
            swsizer = wx.BoxSizer(wx.VERTICAL)
            for title in titles:
                line = title + "\n"+ stories[title]
                hl.HyperLinkCtrl(panel,-1,title, pos=(45,start), URL=stories[title])
                start += 25
            wx.StaticText(panel, -1, "", (start, 25))
            wx.Button(panel, -1, 'Exit', (start+25, 370))
            self.Bind(wx.EVT_BUTTON, self.OnClose)
            swsizer.Add(panel, 0, wx.ALL, 25)
            self.sw.SetSizer(swsizer)
            self.sw.EnableScrolling(True, True)
            self.sw.SetScrollRate(1,1)
        self.Show()
    
    def OnSize(self, event):
        self.sw.SetSize(self.GetClientSize())
    
    def OnClose(self,event):
        self.Destroy()
        sys.exit(0)
