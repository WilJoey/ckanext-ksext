# -*- coding: utf-8 -*-

import ckan.plugins as p
from ckan.lib.base import BaseController, config
import ckan.lib.helpers as h
import ckan.model as model
import collections
import uuid
from ckan.common import response, request, json

class DatasetsController(BaseController):
    
    def index (self, id=None):
        c = p.toolkit.c
        
        #try:
        sql = u'''
SELECT p.id, p.name, p.title, p.url, p.notes, p.maintainer, p.maintainer_email, l.title as license,
  (select value from package_extra where package_id=p.id and key='資料集類型' and state='active') as extra0,
  (select value from package_extra where package_id=p.id and key='資料量' and state='active') as extra1,
  (select value from package_extra where package_id=p.id and key='計費方式' and state='active') as extra3,
  g.id as org_id, g.name as org_name, g.title as org_title,
  to_char(p.metadata_modified, 'YYYY-MM-DD HH24:MI:SS') as modified
FROM public."package" p LEFT OUTER JOIN public."license" l on l.id=p.license_id, public."group" g
WHERE p.owner_org = g.id AND p.state='active' AND p.private = FALSE AND g.state='active' 
ORDER BY p.metadata_modified DESC ; '''
        _ViewCount = collections.namedtuple("ViewCount", "id name title url notes maintainer maintainer_email license extra0 extra1 extra3 org_id org_name org_title modified")
        engine = model.meta.engine
        result = [_ViewCount(*t) for t in engine.execute(sql).fetchall()]
        model.meta.engine.execute(sql)

        limit = int(request.params.get('limit', 0))
        if limit != 0: 
            result = result[:limit]
        
        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(result)
