from flask import Flask, url_for, redirect,render_template, request
import os, sys
basepath = os.getcwd()+os.path.sep+r".."
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

cache_keywords = []
@app.route('/', methods=['POST','GET'])
def main_page():
    error = None
    if request.method=='POST':
        item= request.form
        return rerouting(item)
    return render_template('index.html')

def rerouting(item):
    if "marketplace" in item:
        return redirect(url_for('.show_entries',source='marketplace'))
    elif "hackernews" in item:
        return redirect(url_for('.show_entries',source='hackernews'))
    elif "buzzfeed" in item:
        return redirect(url_for('.data_input',source=item.keys()[0]))
    else:
        return redirect(url_for('.data_input',source=item.keys()[0]))

@app.route('/buzzfeed/data', methods=['POST','GET'])
def bzfd_input():
    global cache_keywords
    static_text = "Select one or more categories"
    if request.method=='POST':
        cache_keywords = request.form.keys()
        print cache_keywords
        return redirect(url_for('.show_entries',source="buzzfeed"))
    return render_template('get_buzzfeed.html',static_text=static_text)

@app.route('/<source>/data', methods=['POST','GET'])
def data_input(source):
    global cache_keywords
    static_text="What would you like to know about?"
    if source == "hackernews":
        static_text="Enter number of stories:"
    if request.method=='POST':
        cache_keywords = [item.strip() for item in request.form['data'].split(',')]
        return redirect(url_for('.show_entries',source=source))
    return render_template('get_optional_data.html',static_text=static_text)

@app.route('/news/<source>', methods=['GET','POST'])
def show_entries(source):
    if request.method=='POST':
        print request.form
        if request.form['home']=='Return to main page':
            return redirect(url_for('.main_page'))
    global cache_keywords
    if source=='marketplace':
        stories = getattr(sys.modules[source], "get_stories")()
    elif source=='hackernews':
        stories = getattr(sys.modules[source], "get_stories")(15)
    else:
        stories = {}
        for word in cache_keywords:
            stories.update(getattr(sys.modules[source], "get_stories")(str(word)))
    try:
        if stories == {}:
            foo=get_placekitten()
            print foo
            return render_template('show_entries.html',entries=foo.encode('utf-8'))
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
