import sys,os

if __name__=="__main__":
    basepath = os.getcwd()
    sys.path.append(basepath+os.path.sep+"libs")
    sys.path.append(basepath+os.path.sep+"restagents")
    sys.path.append(basepath+os.path.sep+"rssagents")
    options = ['nytimes','washpost','nprnews','marketplace','buzzfeed','hackernews']
    i = 1
    for option in options:
        print "%d: %s" % (i, option)
        i+=1
    n = int(raw_input("Enter your choice:\t"))
    __import__("%s"%options[n-1])
    #getattr(sys.modules[options[n-1]], "get_stories")()
    getattr(sys.modules[options[n-1]], "main")()
