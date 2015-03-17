from datetime import date
import wx,sys
import wx.lib.agw.hyperlink as hl

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


class Results(wx.Frame):
    def __init__(self, parent, id, title, stories):
        wx.Frame.__init__(self, parent, id, title,size=(500,400))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
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
        swsizer.Add(panel, 0, wx.ALL, 25)
        self.sw.SetSizer(swsizer)
        self.sw.EnableScrolling(True, True)
        self.sw.SetScrollRate(1,1)
        self.Show()
    
    def OnSize(self, event):
        self.sw.SetSize(self.GetClientSize())
    
    def OnClose(self,event):
        self.Destroy()
        sys.exit()
        
