import constants
from ckan.plugins import toolkit as tk

@tk.auth_allow_anonymous_access
def suggest_index(context, data_dict):
    return {'success': True}

@tk.auth_allow_anonymous_access
def suggest_create(context, data_dict):
    return {'success': True}

@tk.auth_allow_anonymous_access
def suggest_show(context, data_dict):
    return {'success': True}


def suggest_comment(context, data_dict):
    return {'success': True}
    
def suggest_comment_update(context, data_dict):
    return {'success': True}