# -*- coding: utf-8 -*-

import constants
import sqlalchemy as sa
import uuid
import logging

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, backref

Suggest = None
Comment = None
log = logging.getLogger(__name__)

def uuid4():
    return str(uuid.uuid4())

def init_db(model):

    global Suggest
    global Comment

    if Suggest is None:

        class _Suggest(model.DomainObject):

            @classmethod
            def get(cls, **kw):
                '''Finds all the instances required.'''
                query = model.Session.query(cls).autoflush(False)
                
                return query.filter_by(**kw).all()

            @classmethod
            def views_plus(cls, id):
                model.Session.execute("UPDATE suggests SET views=views+1 WHERE id=:id", {'id': id})
                model.Session.commit()
                return False

            @classmethod
            def suggest_mailed(cls, id):
                #log.warn('joe db: suggest_mailed : ' + id)
                sql = 'UPDATE suggests SET send_mail=1 WHERE id=:id;'
                model.Session.execute(sql, {'id': id})
                model.Session.commit()

                sql = 'UPDATE suggests SET mail_time=CURRENT_TIMESTAMP WHERE id=:id AND mail_time is null AND send_mail=1;'
                model.Session.execute(sql, {'id': id})
                model.Session.commit()
                
                #log.warn('joe db: committed : ' + id)
                return True

            @classmethod
            def suggest_exists(cls, title):
                '''Returns true if there is a Data Request with the same title (case insensitive)'''
                query = model.Session.query(cls).autoflush(False)

                return query.filter(func.lower(cls.title) == func.lower(title)).first() is not None

            @classmethod
            def get_ordered_by_date(cls, **kw):
                sql='''
SELECT s.id, user_id, s.title, open_time, s.views | 1 as views1, org_id, g.title as org, g.mail_time, s.mail_id,
   (select count(*) from suggests_comments where suggest_id = id) as comments 
FROM  suggests s left join "group" g on s.org_id=g.id
WHERE closed=False ORDER BY open_time DESC ;
                '''
                query = model.Session.query(cls).autoflush(False)
                return query.filter_by(**kw).order_by(cls.open_time.desc()).all()



            # @classmethod
            # def query_by_sql(cls, **kw):
            #     sql = "SELECT id, user_id, title, open_time, views, (select count(*) from suggests_comments where suggest_id = id) as comments FROM  suggests WHERE closed=False ORDER BY open_time DESC"
            #     return None

        Suggest = _Suggest

        # FIXME: References to the other tables...
        suggests_table = sa.Table('suggests', model.meta.metadata,
            sa.Column('user_id', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('id', sa.types.UnicodeText, primary_key=True, default=uuid4),
            sa.Column('title', sa.types.UnicodeText(constants.NAME_MAX_LENGTH), primary_key=True, default=u''),
            sa.Column('description', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('dataset_name', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('suggest_columns', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('open_time', sa.types.DateTime, primary_key=False, default=None),
            sa.Column('views', sa.types.Integer, primary_key=False, default=0),
            sa.Column('close_time', sa.types.DateTime, primary_key=False, default=None),
            sa.Column('closed', sa.types.Boolean, primary_key=False, default=False),
            sa.Column('org_id', sa.types.UnicodeText, primary_key=False, default=False),
            sa.Column('send_mail', sa.types.Integer, primary_key=False, default=0),
            sa.Column('mail_time', sa.types.DateTime, primary_key=False, default=None),
            sa.Column('email', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('mail_id', sa.types.UnicodeText, primary_key=False, default=None)
        )
        #suggests_table.comments = relationship('suggests_comments', backref='suggests')

        # Create the table only if it does not exist
        suggests_table.create(checkfirst=True)

        model.meta.mapper(Suggest, suggests_table,)


    if Comment is None:
        class _Comment(model.DomainObject):

            @classmethod
            def get(cls, **kw):
                '''Finds all the instances required.'''
                query = model.Session.query(cls).autoflush(False)
                
                return query.filter_by(**kw).all()

            @classmethod
            def get_ordered_by_date(cls, **kw):
                '''Personalized query'''
                query = model.Session.query(cls).autoflush(False)
                return query.filter_by(**kw).order_by(cls.time.desc()).all()

            @classmethod
            def get_count_by_suggest(cls, **kw):
                query = model.Session.query(cls).autoflush(False)
                return query.filter_by(**kw).count()

        Comment = _Comment

        # FIXME: References to the other tables...
        comments_table = sa.Table('suggests_comments', model.meta.metadata,
            sa.Column('id', sa.types.UnicodeText, primary_key=True, default=uuid4),
            sa.Column('user_id', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('suggest_id', sa.types.UnicodeText, primary_key=True, default=uuid4),
            sa.Column('time', sa.types.DateTime, primary_key=True, default=u''),
            sa.Column('comment', sa.types.UnicodeText, primary_key=False, default=u'')
        )

        # Create the table only if it does not exist
        comments_table.create(checkfirst=True)

        model.meta.mapper(Comment, comments_table,)
