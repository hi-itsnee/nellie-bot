import wx, sys, os
basepath = os.getcwd()+os.path.sep+".."
sys.path.append(basepath)
sys.path.append(basepath+os.path.sep+"libs")
sys.path.append(basepath+os.path.sep+"restagents")
sys.path.append(basepath+os.path.sep+"rssagents")
from printing_helper import *
from config_helper import *
from rest import *
from rss import *
import hackernews, nprnews, nytimes, washpost
import buzzfeed, marketplace
import wx.lib.agw.hyperlink as hl

name_map={'The New York Times': 'nytimes', "Washington Post": 'washpost', "NPR News": "nprnews", "Buzzfeed":'buzzfeed', "Marketplace":'marketplace','HackerNews':'hackernews'}

app = wx.App(0)
app_title = 'NellieBot - A simple news aggregator'
class FirstPage(wx.Dialog):
    boxes = []
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(250, 300))
        wx.StaticBox(self, -1, "Select your news source: ",(5,15),size=(230,240))
        self.options = ["The New York Times", "Washington Post", "NPR News"]
        self.options.append("Buzzfeed")
        self.options.append("Marketplace")
        self.options.append("HackerNews")
        #add_options(options, self)
        wx.ComboBox(self,-1,pos=(50,100),size=(150,-1),choices=self.options,style=wx.CB_READONLY)
        wx.Button(self, 1, 'Exit', (70, 215))
        self.Bind(wx.EVT_BUTTON, self.OnClose, id=1)
        #self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        self.Centre()
        self.ShowModal()
    def OnSelect(self, event):
        self.Close()
        self.Destroy()
        self.me = name_map[self.options[event.GetSelection()]]
        run_agents(self.me)
    def OnClose(self, events):
        sys.exit(0)

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
        
class Bzfd_category(wx.Dialog):
    boxes = []
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, app_title, size=(250, 300))
        wx.StaticBox(self, -1, "Select category: ",(5,5),size=(240,200))
        options = ["Homepage", "USNews", "Animals", "Tech", "Entertainment"]
        options.append("Sports")
        add_options(options, self)
        wx.Button(self, 1, 'Submit', (70, 215))
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()
        self.Centre()
        self.ShowModal()
    def OnSubmit(self, events):
        self.Destroy()
        keywords = []
        for box in self.boxes:
            if box.IsChecked():
                keywords.append(box.GetLabelText().lower())
        run_keyword_agent("buzzfeed",keywords)
    def OnClose(self, events):
        sys.exit(0)

class KeywordMenu(wx.Dialog):
    boxes = []
    def __init__(self, parent, id, title, source):
        wx.Dialog.__init__(self, parent, id, app_title, size=(250, 300))
        self.source=source
        wx.StaticText(self, -1, "Enter one or more search terms",pos=(40,60),style=wx.ALIGN_CENTER)
        wx.StaticText(self, -1, "(Seperated by commas)", pos=(55,100),style=wx.ALIGN_CENTER)
        self.textbox=wx.TextCtrl(self, -1, "", pos=(50,150),size=(140,-1))
        wx.Button(self, 1, 'Submit', (70, 215))
        self.Bind(wx.EVT_BUTTON, self.OnSubmit, id=1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Centre()
        self.Centre()
        self.ShowModal()
    def OnSubmit(self, events):
        self.Destroy()
        line = self.textbox.GetLineText(0)
        keywords = line.split(',')
        run_keyword_agent(self.source,keywords)
    def OnClose(self, events):
        sys.exit(0)

def run_agents(item):
    __import__("%s"%item)
    if item=='marketplace':
        stories=getattr(sys.modules[item], "get_stories")()
        Results(None,-1,app_title,stories)
        app.MainLoop()
    elif item=='hackernews':
        stories=getattr(sys.modules[item], "get_stories")(15)
        Results(None,-1,app_title,stories)
        app.MainLoop()
        #stories=HNcount()
    elif item=='washpost' or item=='nprnews' or item=='nytimes':
        KeywordMenu(None, -1, 'Enter keyword to search', item)
    else:
        Bzfd_category(None, -1, 'Select Buzzfeed Category')

def run_keyword_agent(mod,keywords):
    stories = {}
    for keyword in keywords:
        stories.update(getattr(sys.modules[mod], "get_stories")(keyword))
    Results(None,-1,app_title,stories)
    app.MainLoop()

def add_options(list_of_options, parent):
    start =  30
    list_of_boxes = []
    for option in list_of_options:
        parent.boxes.append(wx.CheckBox(parent, -1,option, (15, start)))
        start += 25

def main():
    FirstPage(None, -1, app_title)
    app.MainLoop()

if __name__=="__main__":
    main()
