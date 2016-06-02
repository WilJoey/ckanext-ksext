# -*- coding: utf-8 -*-

import constants
import ckan.plugins.toolkit as tk
import dbsuggest as db


def validate_suggest(context, request_data):

    errors = {}

    # Check user_id
    if not request_data['user_id']:
        errors['UserId'] = [tk._('User name cannot be empty')]
    if len(request_data['user_id']) > constants.NAME_MAX_LENGTH:
        errors['UserId'] = [tk._('User name must be a maximum of %d characters long') % constants.NAME_MAX_LENGTH]

    # Check name
    if len(request_data['title']) > constants.NAME_MAX_LENGTH:
        errors['Title'] = [tk._('Title must be a maximum of %d characters long') % constants.NAME_MAX_LENGTH]

    if not request_data['title']:
        errors['Title'] = [tk._('Title cannot be empty')]

    # Title is only checked in the database when it's correct
    avoid_existing_title_check = context['avoid_existing_title_check'] if 'avoid_existing_title_check' in context else False

    if 'Title' not in errors and not avoid_existing_title_check:
        if db.Suggest.suggest_exists(request_data['title']):
            errors['Title'] = [u'此標題已存在']
            

    # Check description
    if len(request_data['description']) > constants.DESCRIPTION_MAX_LENGTH:
        errors['Description'] = [tk._('Description must be a maximum of %d characters long') % constants.DESCRIPTION_MAX_LENGTH]


    if len(errors) > 0:
        raise tk.ValidationError(errors)


def validate_suggest_closing(context, request_data):
    pass



def validate_comment(context, request_data):
    comment = request_data.get('comment', '')

    # Check if the data request exists
    try:
        tk.get_action(constants.SUGGEST_SHOW)(context, {'id': request_data['suggest_id']})
    except Exception:
        raise tk.ValidationError({'Data Request': [tk._('Data Request not found')]})

    if not comment or len(comment) <= 0:
        raise tk.ValidationError({'Comment': [tk._('Comments must be a minimum of 1 character long')]})

    if len(comment) > constants.COMMENT_MAX_LENGTH:
        raise tk.ValidationError({'Comment': [tk._('Comments must be a maximum of %d characters long') % constants.COMMENT_MAX_LENGTH]})

