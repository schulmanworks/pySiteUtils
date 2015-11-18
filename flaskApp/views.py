__author__ = 'ryan'
from flaskApp import app
from flask import render_template, request
from .forms import URLForm
from main import run, spellCheckTree,processSpellCheck
@app.route('/')
def index():
    form = URLForm()
    return render_template('index.html',title='Home',form=form)
@app.route('/',methods=['POST'])
def processInput():
    url = request.form['url']
    domain = request.form['domain']
    if url != "" and url is not None:
        root=run(url,domain)#this run from main.py not run.py
        pages = spellCheckTree(root)
        #arr = processSpellCheck(pages)
        return render_template('validation.html',title="validation",elems=pages)
    else:
        return "You entered nothing"