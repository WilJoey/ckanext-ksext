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
import logging
import pylons

from ckanext.ksext import helpers
import ckanext.ksext.controllers.twod as twod

log = logging.getLogger(__name__)


class TnStatsController(BaseController):
    def _get_context(self):
        return {'model': model, 'session': model.Session,
                'user': toolkit.c.user, 'auth_user_obj': toolkit.c.userobj}    

    def orgs(self):
        result = helpers.get_org_list()
        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(result)
        
    def meta(self):

        #message = twod.meta_dataset_publish_create(self._get_context(), 'test-meta-create-3')
        message = 'google user session'
        meta_status = helpers.is_gauth_login()
        #meta_status = False
        #if 'ckanext-google-user' in pylons.session:
        #    meta_status = True

        result ={'success': meta_status, 'message': message}
        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(result)


    def ranking(self):
        dataset_id = request.params.get('dataset_id',None)
        dataset_name = request.params.get('dataset_name', None)
        user_star = request.params.get('user_star', None)
        user_id = toolkit.c.userobj.id
        '''
        log.error('JJOOEE,dataset_id: ' + dataset_id)
        log.error('JJOOEE,dataset_name: ' + dataset_name)
        log.error('JJOOEE,user_star: ' + user_star)
        log.error('JJOOEE,user_id: ' + toolkit.c.userobj.id)
        '''
        cnt = self._get_user_star(dataset_id, user_id)
        if (cnt==0):
            self._ranking_insert(dataset_id, user_id, user_star)
        else:
            self._ranking_update(dataset_id, user_id, user_star)

        h.redirect_to(controller='package', action='read', id=dataset_name)

    def _get_user_star(self, dataset_id, user_id):
        engine = model.meta.engine
        sql = '''
SELECT count(*) FROM ranking WHERE package_id=%s AND user_id=%s;
        '''
        result = engine.execute(sql, dataset_id, user_id).fetchall()
        if (len(result) == 0):
            return 0
        else :
            return result[0][0]

    def _ranking_insert(self, dataset_id, user_id, user_star):
        engine = model.meta.engine
        sql = '''
INSERT INTO ranking (package_id, user_id, stars) 
VALUES (%s, %s, %s);
        '''
        engine.execute(sql, dataset_id, user_id, user_star)

    def _ranking_update(self, dataset_id, user_id, user_star):
        engine = model.meta.engine
        sql = '''
UPDATE ranking SET stars=%s
WHERE  package_id=%s, user_id=%s
        '''
        engine.execute(sql, user_star, dataset_id, user_id)

    def index (self):
        c = p.toolkit.c

        ## Used by the Tracking class
        _ViewCount = collections.namedtuple("ViewCount", "id title name org_name dataset_views resource_views resource_downloads")

        engine = model.meta.engine
        sql = '''
SELECT p.id, p.title, p.name,
    (SELECT title FROM "group" WHERE id=p.owner_org) AS org_name,
    COALESCE(SUM(s.count), 0) AS dataset_views, 
    COALESCE((SELECT SUM(resource_count) FROM v_dataset_count WHERE dataset_id=p.id), 0) AS resource_views,
    COALESCE((SELECT SUM(resource_count) FROM v_dataset_download WHERE dataset_id=p.id), 0) AS resource_downloads
FROM package AS p
    LEFT OUTER JOIN tracking_summary AS s ON s.package_id = p.id
WHERE p.state='active'
GROUP BY p.id, p.title
ORDER BY org_name ASC; '''
        c.datasets_count =  [_ViewCount(*t) for t in engine.execute(sql).fetchall()]

        return p.toolkit.render('tnstats/index.html')

    def group (self):
        c = p.toolkit.c
        
        ## Used by the Tracking class
        _ViewCount = collections.namedtuple("ViewCount", "id title name group_name dataset_views resource_views resource_downloads")

        engine = model.meta.engine
        sql = '''
SELECT p.id, p.title, p.name, g.title as group_name, 
  COALESCE(SUM(s.count), 0) AS dataset_views,
  COALESCE((SELECT SUM(resource_count) FROM v_dataset_count WHERE dataset_id=p.id), 0) AS resource_views,
  COALESCE((SELECT SUM(resource_count) FROM v_dataset_download WHERE dataset_id=p.id), 0) AS resource_downloads
FROM 
  public."package" p LEFT OUTER JOIN tracking_summary AS s ON s.package_id = p.id, 
  public.member m, 
  public."group" g
WHERE 
  m.table_id = p.id AND g.id = m.group_id AND 'active' = p.state AND false = g.is_organization
GROUP BY
  p.id, g.id
ORDER BY
  g.title ASC, 
  p.title ASC; '''
        c.datasets_count =  [_ViewCount(*t) for t in engine.execute(sql).fetchall()]

        return p.toolkit.render('tnstats/group.html')

    def keyword (self):
        c = p.toolkit.c

        ## Used by the Tracking class
        _ViewCount = collections.namedtuple("ViewCount", "content count")

        engine = model.meta.engine
        sql = '''
SELECT content, COUNT(content) as count
FROM v_keyword_filtered
GROUP BY content ORDER BY count DESC, content ASC; '''
        c.keyword_count =  [_ViewCount(*t) for t in engine.execute(sql).fetchall()]
        return p.toolkit.render('tnstats/keyword.html')

    def kwfilter(self):
        c = p.toolkit.c
        result = {}
        result['status']=True
        result['message']= ''
        sql = '''
SELECT content, COUNT(content) as count
FROM v_keyword_filtered
WHERE created between %s and  %s
GROUP BY content ORDER BY count DESC, content ASC; '''

        if(request.params.get('all',False)):
            sql ='''
SELECT content, COUNT(content) as count
FROM v_keyword_filtered
GROUP BY content ORDER BY count DESC, content ASC; '''
        
        try:
            result['strat']=request.params.get('start',None)
            result['end']=request.params.get('end',None)
            ## Used by the Tracking class
            _ViewCount = collections.namedtuple("ViewCount", "content count")

            engine = model.meta.engine
            result['data'] = [_ViewCount(*t) for t in engine.execute(sql, result['strat'], result['end']).fetchall()]

        except sqlalchemy.exc.DataError as e:
            result['status']=False
            result['message']= 'Error: Start or end parameter format incorrect!'
            result['data']=[]

        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(result)

    def _orgApiResult(self):
        engine = model.meta.engine
        sql = '''
SELECT p.id, p.title, p.name,
    (SELECT title FROM "group" WHERE id=p.owner_org) AS org_name,
    COALESCE(SUM(s.count), 0) AS dataset_views, 
    COALESCE((SELECT SUM(resource_count) FROM v_dataset_count WHERE dataset_id=p.id), 0) AS resource_views,
    COALESCE((SELECT SUM(resource_count) FROM v_dataset_download WHERE dataset_id=p.id), 0) AS resource_downloads
FROM package AS p 
LEFT OUTER JOIN tracking_summary AS s ON s.package_id = p.id
WHERE p.state='active' '''

        pid = request.params.get('id', None)
        if(pid):
            sql += ' and p.owner_org=%s '

        sql += '''
GROUP BY p.id, p.title
ORDER BY org_name ASC; '''

        result = engine.execute(sql, pid).fetchall()
        return result

    def _groupApiResult(self):
        engine = model.meta.engine
        sql = '''
SELECT p.id, p.title, p.name, g.title as group_name, 
  COALESCE(SUM(s.count), 0) AS dataset_views,
  COALESCE((SELECT SUM(resource_count) FROM v_dataset_count WHERE dataset_id=p.id), 0) AS resource_views,
  COALESCE((SELECT SUM(resource_count) FROM v_dataset_download WHERE dataset_id=p.id), 0) AS resource_downloads
FROM 
  public."package" p LEFT OUTER JOIN tracking_summary AS s ON s.package_id = p.id, 
  public.member m, 
  public."group" g
WHERE 
  m.table_id = p.id AND g.id = m.group_id AND 'active' = p.state AND false = g.is_organization '''

        pid = request.params.get('id', None)
        if(pid):
            sql += ' and g.id=%s '

        sql += ''' 
GROUP BY
  p.id, g.id
ORDER BY
  g.title ASC, 
  p.title ASC; '''
        result = engine.execute(sql, pid).fetchall()
        return result

    def orgApi (self):
        _ViewCount = collections.namedtuple("ViewCount", "id title name org_name dataset_views resource_views resource_downloads")
        data = self._orgApiResult()
        result = [_ViewCount(*t) for t in data]
        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(result)

    def groupApi (self):
        _ViewCount = collections.namedtuple("ViewCount", "id title name group_name dataset_views resource_views resource_downloads")
        data = self._groupApiResult()
        result =  [_ViewCount(*t) for t in data]

        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(result)

    def csvTest(self):
        result = self._groupApiResult()
        data = u'\ufeff群組,資料集,資料集編碼,資料集瀏覽次數,資料瀏覽次數,資料下載次數\r\n'
        csvFormatter = u'"{0}","{1}","{2}",{3},{4},{5}\r\n'
        for item in result:
            #data += csvFormatter.format(*item)
            data += csvFormatter.format(item[3],item[1],item[2],item[4],item[5],item[6])
        return data

    def orgCsv(self):
        head = u'\ufeff組織,資料集,資料集編碼,資料集瀏覽次數,資料瀏覽次數,資料下載次數\r\n'
        data = self._orgApiResult()
        return self._csv(head, data)

    def groupCsv(self):
        head = u'\ufeff群組,資料集,資料集編碼,資料集瀏覽次數,資料瀏覽次數,資料下載次數\r\n'
        data = self._groupApiResult()
        return self._csv(head, data)

    def _csv(self, head, data):
        base.response.headers['Content-type'] ='text/csv; charset=utf-8'
        base.response.headers['Content-disposition'] ='attachment;filename=statistics.csv'
        
        csvFormatter = u'"{0}","{1}","{2}",{3},{4},{5}\r\n'
        for item in data:
            #data += csvFormatter.format(*item)
            head += csvFormatter.format(item[3],item[1],item[2],item[4],item[5],item[6])
        return head


