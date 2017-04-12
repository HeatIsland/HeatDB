import webapp2
import logging
import re
import cgi
import jinja2
import os
import random
import string
import hashlib
import hmac
import Cookie 
import urllib2
import time
from datetime import datetime, timedelta
from google.appengine.api import memcache
from google.appengine.ext import db
from xml.dom import minidom


## see http://jinja.pocoo.org/docs/api/#autoescaping
def guess_autoescape(template_name):
   if template_name is None or '.' not in template_name:
      return False
      ext = template_name.rsplit('.', 1)[1]
      return ext in ('html', 'htm', 'xml')

JINJA_ENVIRONMENT = jinja2.Environment(
   autoescape=guess_autoescape,     ## see http://jinja.pocoo.org/docs/api/#autoescaping
   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
   extensions=['jinja2.ext.autoescape'])
   
   
class MyHandler(webapp2.RequestHandler):
   def write(self, *items):    
      self.response.write(" : ".join(items))

   def render_str(self, template, **params):
      tplt = JINJA_ENVIRONMENT.get_template('templates/'+template)
      return tplt.render(params)

   def render(self, template, **kw):
      self.write(self.render_str(template, **kw))

   def render_json(self, d):
      json_txt = json.dumps(d)
      self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
      self.write(json_txt)
   
class MainPage(MyHandler):
   def get(self):   
   
application = webapp2.WSGIApplication([
                               ('/', MainPage),],debug=True)
