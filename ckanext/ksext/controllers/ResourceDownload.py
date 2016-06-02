import ckan.plugins as p
from ckan.lib.base import BaseController, config
import ckan.lib.helpers as h
import ckan.model as model
import collections
import uuid
from ckan.common import response, request, json

class ResourceDownloadController(BaseController):
    
    def create (self, id=None):
        c = p.toolkit.c
        result = {}
        result['status']=True
        try:
            uid=uuid.UUID(id)
            result['resource_id']=str(uid)
            
            # store key/data here
            sql = '''INSERT INTO tracking_raw
                     (user_key, url, tracking_type)
                     VALUES (%s, %s, 'download')'''
            model.meta.engine.execute(sql, str(uuid.uuid4()), id)


        except ValueError as e:
            result['status']=False
            result['resource_id']=''
        
        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(result)
