__author__ = 'ryan'
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class URLForm(Form):
    url = StringField('url',validators=[DataRequired()])
    domain = StringField('domain',validators=[DataRequired()])