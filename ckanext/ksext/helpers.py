# -*- coding: utf-8 -*-

import logging
import ckan.model as model
import ckan.logic as logic
import pylons

from ckan.plugins import toolkit as tk

c = tk.c
engine = model.meta.engine
log = logging.getLogger(__name__)

def get_org_list():
    sql = '''
SELECT id, name, title FROM "group" 
WHERE state='active' AND approval_status='approved' 
    AND is_organization=true
ORDER BY title;
    '''
    data = engine.execute(sql).fetchall()
    result = []
    for d in data:
        org = {
            'id':d[0],
            'name': d[1],
            'title': d[2]
        }
        result.append(org)

    return result


def is_gauth_login():
    is_gauth = False
    if 'ckanext-google-user' in pylons.session:
        is_gauth = True
    return is_gauth


def rank_dataset_ranking(package_id):
    result = _get_dataset_ranking(package_id)
    return result

def rank_user_star(dataset_id, user_id):
    #return tk.literal('<!-- No qa info for this dataset -->')
    #log.warning('jjooee:' + dataset.__repr__())

    result = _get_user_dataset_score(dataset_id , user_id)
    return result


def _get_dataset_ranking(package_id):
    #_namedTuple = collections.namedtuple("package_rank", "id title name org_name dataset_views resource_views resource_downloads")
    sql = '''
SELECT avg(stars) as stars FROM ranking WHERE package_id= %s;
    '''
    result = engine.execute(sql, package_id).fetchall()
    if (len(result) == 0) :
        return 0
    else :
        return result[0][0]

def _get_user_dataset_score(package_id, user_id):
    sql = '''
SELECT stars FROM ranking WHERE package_id=%s AND user_id=%s;
    '''
    result = engine.execute(sql, package_id, user_id).fetchall()
    if (len(result) == 0 ) :
        return -1
    else :
        return result[0][0]

def suggest_org_list():
    result = logic.get_action('organization_list')({}, {})
    return result

def get_latest_news():
    sql = '''
SELECT id, title, content, name, group_id 
FROM ckanext_pages 
WHERE private=false AND page_type='page' 
ORDER BY publish_date DESC LIMIT 2;
    '''
    out = engine.execute(sql).fetchall()
    result = []
    for data in out:
        pg = {
            'id': data[0],
            'title': data[1],
            'content': data[2],
            'name': data[3],
            'group_id': data[4]
        }
        result.append(pg)
    return result




'''
def qa_openness_stars_dataset_html(dataset):
    qa = dataset.get('qa')
    if not qa:
        return tk.literal('<!-- No qa info for this dataset -->')
    extra_vars = copy.deepcopy(qa)
    return tk.literal(
        tk.render('qa/openness_stars_brief.html',
                  extra_vars=extra_vars))
'''
