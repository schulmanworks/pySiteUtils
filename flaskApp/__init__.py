__author__ = 'ryan'
from flask import Flask
from main import uccsDictFilter
app = Flask(__name__)
app.config.from_object('config')
from flaskApp import views

def parseSpellChecker(chkr):
    temp = []
    for c in chkr:
        temp.append(c.word)
    badwords = []
    for word in filter(uccsDictFilter,temp):
        badwords.append(word)
    return badwords

app.jinja_env.globals.update(parseSpellChecker=parseSpellChecker)
