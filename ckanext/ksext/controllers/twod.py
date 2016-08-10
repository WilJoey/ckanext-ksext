# -*- coding: utf-8 -*-

import logging
import ckan.model as model
import ckan.logic as logic

from pylons import config
from ckan.plugins import toolkit as toolkit

c = toolkit.c
log = logging.getLogger(__name__)
PUBLISH_CITY_CODE = '397000000A'

#class metapublish:
def meta_resouce_serial_update(id, package_id):
    #log.warn('twod: meta_resource_serial_update')
    sql = '''
UPDATE resource set meta_no=(
  SELECT MAX(meta_no)+1 FROM resource WHERE package_id=%s 
) WHERE id=%s;
'''
    model.meta.engine.execute(sql, id, package_id)


def meta_dataset_publish(context, package_id):
    
    package = logic.get_action('package_show')(context, {'id': package_id})
    #log.warn('twod publish before:' + package.__repr__())
    site_url = config.get('ckan.site_url', '')
    log.warn('twod publish site_url: ' + site_url.__repr__())
    tags = package['tags']

    meta = {
        'organization': '高雄市政府',
        'organizationContactName': '高雄市政府',
        'organizationContactPhone': '07-3368333',
        'organizationContactEmail': 'opendatasys@kcg.gov.tw'
    }
    extras = package['extras']
    meta['categoryCode']=_meta_get_extras_key(extras, u'服務分類')
    meta_no = _meta_get_package_meta_no(package_id)
    package_code = str(meta_no).zfill(6)
    meta['categoryCode'] = PUBLISH_CITY_CODE + package_code
    #meta['']=package['']
    #meta['']=_meta_get_extras_key(extras, u'')
    meta['title']=package['title']
    meta['description']=package['notes']
    meta['fieldDescription']=''
    #resources = _meta_get_resources(package['id'], package_code)
     
    resources = package['resources']
    if (len(resources)>0):
        meta['fieldDescription']=resources[0]['description']
    meta['type']=_meta_get_extras_key(extras, u'資料量')
    meta['license']=package['license_title']
    meta['licenseURL']=package['license_url']
    meta['cost']=_meta_get_extras_key(extras, u'計費方式')
    meta['costURL']=''
    meta['publisher']=''
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
    meta['spatial']=''
    meta['language']=''
    meta['landingPage'] = site_url + '/dataset/' + package['title']
    meta['keyword'] = [tag['display_name'] for tag in tags]
    meta['numberOfData']=_meta_get_extras_key(extras, u'資料量')
    meta['notes']=''
    meta['distribution'] = _meta_get_resources(package, package_code, site_url)
    log.warn('twod publish meta:' + meta.__repr__())
    

def _meta_get_resources(package, package_code, site_url):
    rmetas = _meta_get_resources_metas(package['id'])
    log.warn('twod publish rmetas2: ' + rmetas.__repr__())

    distributs = []
    for resource in package['resources']:
        data = {}
        #meta['categoryCode'] = PUBLISH_CITY_CODE + package_code
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

def _meta_get_resource_code(rmetas, resource_id):
    for m in rmetas:
        if m['id'] == resource_id:
            return m['meta_no']
    return 0

def _meta_get_resources_metas(package_id):
    sql = '''
SELECT id, meta_no FROM resource WHERE package_id=%s ;
'''
    dt = model.meta.engine.execute(sql, package_id).fetchall()
    result = [dict(row) for row in dt]
    return result

    #result = []
    #for row in dt:
    #   result.append(dict(row))
    #return result

def _meta_get_extras_key(extras, key):
    for extra in extras:
        if extra['key']==key:
            return extra['value']
    return ''

def _meta_get_package_meta_no(package_id):
    sql = '''
SELECT meta_no FROM package WHERE id=%s ;
    '''
    result = model.meta.engine.execute(sql, package_id).fetchall()
    if (len(result) == 0 ) :
        return 0 
    else :
        return result[0][0]


'''
#)table package add column meta_no
ALTER TABLE resource ADD COLUMN meta_no serial NOT NULL ;

#resource add column meta_no 
ALTER TABLE resource ADD COLUMN meta_no integer NOT NULL DEFAULT 0;
# resource update meta_no
CREATE TEMP TABLE temp1 AS
SELECT id AS rid, package_id, row_number() OVER (PARTITION BY package_id ORDER BY created) AS rnum
FROM resource
ORDER BY created;
UPDATE resource
SET meta_no = (SELECT rnum FROM temp1 WHERE temp1.rid=id);

DROP TABLE temp1;

'''
