import constants
import sqlalchemy as sa
import uuid

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship, backref

Suggest = None
Comment = None


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
            def suggest_exists(cls, title):
                '''Returns true if there is a Data Request with the same title (case insensitive)'''
                query = model.Session.query(cls).autoflush(False)

                return query.filter(func.lower(cls.title) == func.lower(title)).first() is not None

            @classmethod
            def get_ordered_by_date(cls, **kw):
                sql = "SELECT id, user_id, title, open_time, views, (select count(*) from suggests_comments where suggest_id = id) as comments FROM  suggests WHERE closed=False ORDER BY open_time DESC"
                #query = model.Session.query(cls).autoflush(False)
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
            sa.Column('description', sa.types.UnicodeText(constants.DESCRIPTION_MAX_LENGTH), primary_key=False, default=u''),
            sa.Column('dataset_name', sa.types.UnicodeText(constants.DATASET_NAME_MAX_LENGTH), primary_key=False, default=u''),
            sa.Column('suggest_columns', sa.types.UnicodeText(constants.SUGGEST_COLUMNS_MAX_LENGTH), primary_key=False, default=u''),
            sa.Column('open_time', sa.types.DateTime, primary_key=False, default=None),
            sa.Column('views', sa.types.Integer, primary_key=False, default=0),
            sa.Column('close_time', sa.types.DateTime, primary_key=False, default=None),
            sa.Column('closed', sa.types.Boolean, primary_key=False, default=False)
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
            sa.Column('comment', sa.types.UnicodeText(constants.COMMENT_MAX_LENGTH), primary_key=False, default=u'')
        )

        # Create the table only if it does not exist
        comments_table.create(checkfirst=True)

        model.meta.mapper(Comment, comments_table,)
