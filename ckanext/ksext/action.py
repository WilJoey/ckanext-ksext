import ckan.plugins as plugins
import ckan.lib.helpers as h
import ckan.logic as logic
import ckan.model as model
import collections
import dbsuggest as db
import constants
import datetime
import cgi
import logging
import validator

from ckan.common import response, request, json

c = plugins.toolkit.c
log = logging.getLogger(__name__)
tk = plugins.toolkit

# Avoid user_show lag
USERS_CACHE = {}

def _get_user(user_id):
    try:
        if user_id in USERS_CACHE:
            return USERS_CACHE[user_id]
        else:
            user = tk.get_action('user_show')({'ignore_auth': True}, {'id': user_id})
            USERS_CACHE[user_id] = user
            return user
    except Exception as e:
        log.warn(e)


def tnstats_dataset_count(self, id):
    _ViewCount = collections.namedtuple("ViewCount", "views downloads")

    engine = model.meta.engine
    sql = '''
SELECT 
    COALESCE(SUM(s.count), 0) AS views,
    --COALESCE((SELECT SUM(resource_count) FROM v_dataset_count WHERE dataset_id=p.id), 0) AS views,
    COALESCE((SELECT SUM(resource_count) FROM v_dataset_download WHERE dataset_id=p.id), 0) AS downloads
FROM package AS p LEFT OUTER JOIN tracking_summary AS s ON s.package_id = p.id
WHERE p.id = %s GROUP BY p.id ; '''
    result = [_ViewCount(*t) for t in engine.execute(sql, id).fetchall()]
    
    return result[0]


def suggest_index(context, data_dict):
    model = context['model']

    # Init the data base
    db.init_db(model)

    # Check access
    tk.check_access(constants.SUGGEST_INDEX, context, data_dict)
    params = {}

    # Filter by state
    closed = data_dict.get('closed', None)
    if closed is not None:
        params['closed'] = closed
    
    # Call the function
    db_suggests = db.Suggest.get_ordered_by_date(**params)

    # Dictize the results
    offset = data_dict.get('offset', 0)
    limit = data_dict.get('limit', constants.SUGGESTS_PER_PAGE)
    suggests = []
    for data_req in db_suggests[offset:offset + limit]:
        suggests.append(_dictize_suggest_list(data_req))
    
    

    result = {
        'count': len(db_suggests),
        'facets': {},
        'result': suggests
    }

    return result

def _dictize_suggest_list(suggest):
    # Transform time
    open_time = str(suggest.open_time)
    close_time = suggest.close_time
    close_time = str(close_time) if close_time else close_time

    data_dict = {
        'id': suggest.id,
        'title': suggest.title,
        'user_id': _star_id(suggest.user_id),
        'open_time': open_time,
        'views': suggest.views,
        'comments' : db.Comment.get_count_by_suggest(suggest_id=suggest.id)
    }
    return data_dict

def _star_id(uid):
    if len(uid) < 3:
        return '**'
    ap = '*'
    for i in uid[1:-1]:
        ap += i
    ap += '*'
    return ap

def suggest_create(context, data_dict):
    model = context['model']
    session = context['session']

    # Init the data base
    db.init_db(model)

    # Check access
    tk.check_access(constants.SUGGEST_CREATE, context, data_dict)

    # Validate data
    validator.validate_suggest(context, data_dict)

    # Store the data
    data_req = db.Suggest()
    _undictize_suggest_basic(data_req, data_dict)

    data_req.open_time = datetime.datetime.now()

    session.add(data_req)
    session.commit()

    return _dictize_suggest(data_req)

def _dictize_suggest(suggest):
    # Transform time
    open_time = str(suggest.open_time)
    # Close time can be None and the transformation is only needed when the
    # fields contains a valid date
    close_time = suggest.close_time
    close_time = str(close_time) if close_time else close_time

    # Convert the data request into a dict
    data_dict = {
        'id': suggest.id,
        #'user_name': suggest.user_name,
        'title': suggest.title,
        'description': suggest.description,
        'user_id': _star_id(suggest.user_id),
        'dataset_name': suggest.dataset_name,
        'suggest_columns': suggest.suggest_columns,

        'open_time': open_time,
        
        'close_time': close_time,
        'closed': suggest.closed,
        'views': suggest.views
    }
    return data_dict



def _undictize_suggest_basic(suggest, data_dict):
    suggest.title = data_dict['title']
    suggest.description = data_dict['description']
    suggest.user_id = data_dict['user_id']
    suggest.dataset_name = data_dict['dataset_name']
    suggest.suggest_columns = data_dict['suggest_columns']
    
def suggest_show(context, data_dict):
    model = context['model']
    suggest_id = data_dict.get('id', '')

    if not suggest_id:
        raise tk.ValidationError('Data Request ID has not been included')

    # Init the data base
    db.init_db(model)

    # Check access
    tk.check_access(constants.SUGGEST_SHOW, context, data_dict)

    # Get the data request
    result = db.Suggest.get(id=suggest_id)
    if not result:
        raise tk.ObjectNotFound('Data Request %s not found in the data base' % suggest_id)

    

    data_req = result[0]

    data_dict = _dictize_suggest(data_req)

    # Get comments
    comments_db = db.Comment.get_ordered_by_date(suggest_id=data_dict['id'])

    comments_list = []
    for comment in comments_db:
        comments_list.append(_dictize_comment(comment))

    data_dict['comments'] = comments_list
    return data_dict    
    
def suggest_views(context, data_dict):
    model = context['model']
    suggest_id = data_dict.get('id', '')
    db.Suggest.views_plus(suggest_id)


def suggest_comment(context, data_dict):
    model = context['model']
    session = context['session']
    suggest_id = data_dict.get('suggest_id', '')

    # Check id
    if not suggest_id:
        raise tk.ValidationError(['Data Request ID has not been included'])

    # Init the data base
    db.init_db(model)

    # Check access
    tk.check_access(constants.SUGGEST_COMMENT, context, data_dict)

    # Validate comment
    validator.validate_comment(context, data_dict)

    # Store the data
    comment = db.Comment()
    _undictize_comment_basic(comment, data_dict)
    comment.user_id = context['auth_user_obj'].id
    comment.time = datetime.datetime.now()

    session.add(comment)
    session.commit()

    return _dictize_comment(comment)

def _undictize_comment_basic(comment, data_dict):
    comment.comment = cgi.escape(data_dict.get('comment', ''))
    comment.suggest_id = data_dict.get('suggest_id', '')


def _dictize_comment(comment):

    return {
        'id': comment.id,
        'suggest_id': comment.suggest_id,
        'user_id': comment.user_id,
        'comment': comment.comment,
        'user': _get_user(comment.user_id),
        'time': str(comment.time)
        
    }
