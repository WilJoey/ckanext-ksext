# -*- coding: utf-8 -*-

import logging
import ckan.model as model
import ckan.logic as logic
import ckan.lib.helpers as h
import requests
import pylons.config as config

#from ckan.common import response, request
from pylons import config
from ckan.plugins import toolkit as toolkit

c = toolkit.c
log = logging.getLogger(__name__)
PUBLISH_CITY_CODE = '397000000A'
_headers = {'Authorization': config.get('ckan.metadata_apikey', '')}

'''
資料新增後，更新 meta_no 序號
'''
def meta_resouce_serial_update(id, package_id):
    #log.warn('twod: meta_resource_serial_update')
    sql = '''
UPDATE resource set meta_no=(
  SELECT MAX(meta_no)+1 FROM resource WHERE package_id=%s 
) WHERE id=%s;
'''
    model.meta.engine.execute(sql, id, package_id)

'''
資料集或資料新增(OR 修改後)，將詮釋資料同步至國發會資料開放平台
'''
def meta_dataset_publish_create(context, package_id):
    package = logic.get_action('package_show')(context, {'id': package_id})
    metadata = _meta_get_metadata(package)

    #將 metadata 資料同步至國發會平台
    json = h.json.dumps(metadata)
    url = 'http://data.nat.gov.tw/api/v1/rest/dataset'
    r = requests.post(url, data=json, headers=_headers)
    log.warn('meta response create:' + r.text)

def meta_dataset_publish_update(context, package_id):
    package = logic.get_action('package_show')(context, {'id': package_id})
    metadata = _meta_get_metadata(package)

    #將 metadata 資料同步至國發會平台
    json = h.json.dumps(metadata)
    url = 'http://data.nat.gov.tw/api/v1/rest/dataset/' + metadata['identifier']
    r = requests.put(url, data=json, headers=_headers)
    log.warn('meta response update:' + r.text)

def meta_dataset_publish_remove(context, package_id):
    meta_no = _meta_get_package_meta_no(package_id)
    identifier = "%s-%s" % (PUBLISH_CITY_CODE, str(meta_no).zfill(6) )

    #將 metadata 資料同步至國發會平台
    url = 'http://data.nat.gov.tw/api/v1/rest/dataset' + identifier
    r = requests.delete(url, headers=_headers)
    log.warn('meta response remove:' + r.text)

'''
將資料集 package_dict 轉換為詮釋資料格式 
'''
def _meta_get_metadata(package):
    package_id = package['id']
    site_url = config.get('ckan.site_url', '')
    tags = package['tags']
    extras = package['extras']
    meta_no = _meta_get_package_meta_no(package_id)
    package_code = str(meta_no).zfill(6)
    resources = package['resources']

    meta = {
        'organization': '高雄市政府',
        'organizationContactName': '高雄市政府',
        'organizationContactPhone': '07-3368333',
        'organizationContactEmail': 'opendatasys@kcg.gov.tw',
        'costURL': '',
        'publisher': '',
        'fieldDescription': '',
        'spatial': '',
        'language': '',
        'notes': ''
    }
    meta['categoryCode']=_meta_get_extras_key(extras, u'服務分類')
    meta['identifier'] ="%s-%s" % (PUBLISH_CITY_CODE, package_code, )
    meta['title']=package['title']
    meta['description']=package['notes']
    if (len(resources)>0):
        meta['fieldDescription']=resources[0]['description']
    meta['type']=_meta_get_extras_key(extras, u'資料量')
    meta['license']=package['license_title']
    meta['licenseURL']=package['license_url']
    meta['cost']=_meta_get_extras_key(extras, u'計費方式')
    if 'organization' in package:
        meta['publisher']=package['organization']['title']
    meta['publisherContactName']=package['maintainer']
    meta['publisherContactPhone']=_meta_get_extras_key(extras, u'提供機關聯絡人電話')
    meta['publisherContactEmail ']=package['maintainer_email']
    meta['accrualPeriodicity']=_meta_get_extras_key(extras, u'更新頻率')
    meta['temporalCoverageFrom']=_meta_get_extras_key(extras, u'收錄期間（起）')
    meta['temporalCoverageTo']=_meta_get_extras_key(extras, u'收錄期間（迄）')
    meta['issued']=package['metadata_created']
    meta['modified']=package['metadata_modified']
    meta['landingPage'] = site_url + '/dataset/' + package['title']
    meta['keyword'] = [tag['display_name'] for tag in tags]
    meta['numberOfData']=_meta_get_extras_key(extras, u'資料量')
    meta['distribution'] = _meta_get_resources(package, package_code, site_url)
    #log.warn('twod publish meta:' + meta.__repr__())
    return meta

'''
取得資料(resource)的詮釋資料格式
'''
def _meta_get_resources(package, package_code, site_url):
    rmetas = _meta_get_resources_metas(package['id'])

    distributs = []
    for resource in package['resources']:
        data = {}
        resource_code = _meta_get_resource_code(rmetas, resource['id'])
        data['resourceID'] = "%s-%s-%s" % (PUBLISH_CITY_CODE, package_code, str(resource_code).zfill(3))
        data['resourceDescription'] = resource['description']
        data['format'] = resource['format']
        data['characterSetCode'] = resource['extras0']
        data['resourceModified'] = resource['extras2']
        data['downloadURL'] = "%s/dataset/%s/resource/%s" % (site_url, package['title'], resource['id'])
        data['metadataSourceOfData'] = ''
        distributs.append(data)
    return distributs

'''
取得資料(resource)的詮釋資料序號
'''
def _meta_get_resource_code(rmetas, resource_id):
    for m in rmetas:
        if m['id'] == resource_id:
            return m['meta_no']
    return 0

'''
取得資料集下所有資料(resource)的詮釋資料序號
'''
def _meta_get_resources_metas(package_id):
    sql = 'SELECT id, meta_no FROM resource WHERE package_id=%s ;'
    dt = model.meta.engine.execute(sql, package_id).fetchall()
    result = [dict(row) for row in dt]
    return result

'''
依照 package extras 的 key 取得值
'''
def _meta_get_extras_key(extras, key):
    for extra in extras:
        if extra['key']==key:
            return extra['value']
    return ''

'''
取得資料集(package)的詮釋資料序號
'''
def _meta_get_package_meta_no(package_id):
    sql = 'SELECT meta_no FROM package WHERE id=%s ;'
    result = model.meta.engine.execute(sql, package_id).fetchall()
    if (len(result) == 0 ) :
        return 0 
    else :
        return result[0][0]

