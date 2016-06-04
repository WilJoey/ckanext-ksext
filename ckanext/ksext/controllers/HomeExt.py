import ckan.plugins as p
from ckan.lib.base import BaseController, config
import ckan.lib.helpers as h
import ckan.model as model
import collections
import sqlalchemy
from ckan.common import response, request, json
import ckan.lib.base as base

class HomeExtController(BaseController):

    def specification(self):
        return base.render('home/specification.html')
        
    def specification_old(self):
        return base.render('home/specification_old.html')

    def guide(self):
        return base.render('home/guide.html')

    def manual(self):
        return base.render('home/manual.html')
    
    def faq(self):
        return base.render('home/faq.html')
