import datetime

from pylons import config
from sqlalchemy import Table, select, func, and_

import ckan.plugins as p
import ckan.model as model

DATE_FORMAT = '%Y-%m-%d'

def table(name):
    return Table(name, model.meta.metadata, autoload=True)

def datetime2date(datetime_):
    return datetime.date(datetime_.year, datetime_.month, datetime_.day)


class Stats(object):
    
    @classmethod
    def most_edited_packages(cls, limit=10):
        package_revision = table('package_revision')
        s = select([package_revision.c.id, func.count(package_revision.c.revision_id)]).\
            group_by(package_revision.c.id).\
            order_by(func.count(package_revision.c.revision_id).desc()).\
            limit(limit)
        res_ids = model.Session.execute(s).fetchall()
        res_pkgs = [(model.Session.query(model.Package).get(unicode(pkg_id)), val) for pkg_id, val in res_ids]
        return res_pkgs

    