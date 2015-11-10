__author__ = 'ryan'
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
from flaskApp import views
