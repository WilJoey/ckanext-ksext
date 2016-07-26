# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import BaseController, config
import ckan.lib.helpers as h
import ckan.model as model
import collections
import sqlalchemy
from ckan.common import response, request, json
import ckan.lib.base as base
import losser.losser as losser
import ckan.plugins.toolkit as toolkit

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
    
    def licenses(self):
        result = []

        license = {}
        license['domain_content']=False
        license['domain_data']=True
        license['domain_software']=False
        license['family']=''
        license['id']='twod_license'
        license['maintainer']=''
        license['od_conformance']='approved'
        license['osd_conformance']='not reviewed'
        license['status']='active'
        license['title']='政府資料開放平臺資料使用規範'
        license['url']='http://data.gov.tw/principle'
        result.append(license)

        license={}
        license['domain_content']=False
        license['domain_data']=True
        license['domain_software']=False
        license['family']=''
        license['id']='ODC-PDDL-1.0'
        license['maintainer']=''
        license['od_conformance']='approved'
        license['osd_conformance']='not reviewed'
        license['status']='active'
        license['title']='Open Data Commons Public Domain Dedication and Licence 1.0'
        license['url']='http://www.opendefinition.org/licenses/odc-pddl'
        result.append(license)

        return h.json.dumps(result)

    

    def _get_context(self):
        return {'model': model, 'session': model.Session,
                'user': toolkit.c.user, 'auth_user_obj': toolkit.c.userobj}


