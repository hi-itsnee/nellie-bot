from flask import Flask, url_for, redirect,render_template, request
import os, sys
basepath = os.getcwd()+os.path.sep+r"..//"
print basepath
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
from werkzeug.debug import get_current_traceback
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])
def main_page():
    error = None
    if request.method=='POST':
        item= request.form
        if "marketplace" in item:
            print item
            return redirect(url_for('.show_entries',source='marketplace'))
        elif "hackernews" in item:
            return redirect(url_for('.show_entries',source='hackernews'))
        elif "buzzfeed" in item:
            print "do nothing for now"
        else:
            return redirect(url_for('.show_entries',source=item.keys()[0]))
    return render_template('index.html')

@app.route('/news/<source>')
def show_entries(source):
    if source=='marketplace':
        stories = getattr(sys.modules[source], "get_stories")()
    elif source=='hackernews':
        stories = getattr(sys.modules[source], "get_stories")(15)
    elif source=="buzzfeed":
        print "do nothing for now"
    else:
        stories = getattr(sys.modules[source], "get_stories")("india")
    try:
        return render_template('show_entries.html', entries=stories)
    except:
        track = get_current_traceback(skip=1,show_hidden_frames=True,
            ignore_system_exceptions=False)
        track.log()

@app.errorhandler(Exception)
def exception_handler(error):
    track = get_current_traceback(skip=1,show_hidden_frames=True,
        ignore_system_exceptions=False)
    track.log()
    return "!!!!" + repr(error)

if __name__=="__main__":
    app.run()
