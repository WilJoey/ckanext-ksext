import logging
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import action as a
import constants
import auth

log = logging.getLogger(__name__)

def ksext_hots(*args):
    '''
    result = {}
    result['arg1'] = args[0] or 'Nothing'
    result['status'] = 'success'
    return result
    '''
    data_dict = {
        'rows': 6,
        'sort': args[0] or 'metadata_modified desc'
    }
    query = plugins.toolkit.get_action('package_search')(None, data_dict)
    return query


# Joe Ksext Plug setup init #
class KsextPlugin(plugins.SingletonPlugin):
    '''tnod plugin.'''
    
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers, inherit=True)
    plugins.implements(plugins.IAuthFunctions)


    ######################################################################
    ############################## IACTIONS ##############################
    ######################################################################
    def get_actions(self):
        return {
            constants.SUGGEST_INDEX: a.suggest_index,
            constants.SUGGEST_CREATE: a.suggest_create,
            constants.SUGGEST_SHOW: a.suggest_show,
            constants.SUGGEST_VIEWS: a.suggest_views,
            # constants.SUGGEST_UPDATE: abc.suggest_update,
            # constants.SUGGEST_DELETE: a.suggest_delete,
            # constants.SUGGEST_CLOSE: a.suggest_close,
            constants.SUGGEST_COMMENT: a.suggest_comment,
            # constants.SUGGEST_COMMENT_LIST: a.suggest_comment_list,
            # constants.SUGGEST_COMMENT_SHOW: a.suggest_comment_show,
            # constants.SUGGEST_COMMENT_UPDATE: a.suggest_comment_update,
            # constants.SUGGEST_COMMENT_DELETE: a.suggest_comment_delete
            constants.SUGGEST_MAILED: a.suggest_mailed,
        }

    ######################################################################
    ########################### AUTH FUNCTIONS ###########################
    ######################################################################
    def get_auth_functions(self):
        return {
            constants.SUGGEST_INDEX: auth.suggest_index,
            constants.SUGGEST_CREATE: auth.suggest_create,
            constants.SUGGEST_SHOW: auth.suggest_show,
            constants.SUGGEST_COMMENT: auth.suggest_comment,
            constants.SUGGEST_COMMENT_UPDATE: auth.suggest_comment_update,
            constants.SUGGEST_MAILED: auth.suggest_mailed,

        }

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'ksext_jscss')
        toolkit.add_public_directory(config, 'public')



    def after_map(self, map):
        map.connect('tnstats', '/tnstats', 
            controller = 'ckanext.ksext.controllers.TnStats:TnStatsController',
            action='index')
    	map.connect('tnstats', '/tnstats/{action}', 
    		controller = 'ckanext.ksext.controllers.TnStats:TnStatsController',
    		action='index')

        map.connect('resource_download','/rsdl/{id}', 
            controller = 'ckanext.ksext.controllers.ResourceDownload:ResourceDownloadController',
            action='create')

        map.connect('muser', '/muser/{action}',
            controller = 'ckanext.ksext.controllers.MUser:MUserController',
            action='index')
        map.connect('muser', '/muser',
            controller = 'ckanext.ksext.controllers.MUser:MUserController',
            action='index')
        map.connect('muser_edit', '/muser/edit/{id:.*}', 
            controller = 'ckanext.ksext.controllers.MUser:MUserController',
            action='edit')
        map.connect('muser_delete', '/muser/delete/{id}', 
            controller = 'ckanext.ksext.controllers.MUser:MUserController',
            action='delete')

        map.connect('datasetlist','/datasetlist', 
            controller = 'ckanext.ksext.controllers.Datasets:DatasetsController',
            action='index')
        
        # HomeExt
        map.connect('home_specification','/specification', 
            controller = 'ckanext.ksext.controllers.HomeExt:HomeExtController', action='specification')
        map.connect('home_specification_old','/specification_old',
            controller = 'ckanext.ksext.controllers.HomeExt:HomeExtController', action='specification_old')
        map.connect('home_guide','/guide', 
            controller = 'ckanext.ksext.controllers.HomeExt:HomeExtController', action='guide')
        map.connect('home_faq','/faq', 
            controller = 'ckanext.ksext.controllers.HomeExt:HomeExtController', action='faq')
        map.connect('home_manual','/manual', 
            controller = 'ckanext.ksext.controllers.HomeExt:HomeExtController', action='manual')
        map.connect('home_licenses','/licenses', 
            controller = 'ckanext.ksext.controllers.HomeExt:HomeExtController', action='licenses') 
        map.connect('home_csv','/csv', 
            controller = 'ckanext.ksext.controllers.HomeExt:HomeExtController', action='csv')


        ## suggests ##
        # Data Requests index
        map.connect('suggests_index', "/suggest",
                  controller='ckanext.ksext.controllers.Suggest:SuggestsController',
                  action='index', conditions=dict(method=['GET']))
        # Create a Data Request
        map.connect('/%s/new' % constants.SUGGESTS_MAIN_PATH,
                  controller='ckanext.ksext.controllers.Suggest:SuggestsController',
                  action='new', conditions=dict(method=['GET', 'POST']))
        # Show a Data Request
        map.connect('suggest_show', '/%s/{id}' % constants.SUGGESTS_MAIN_PATH,
                  controller='ckanext.ksext.controllers.Suggest:SuggestsController',
                  action='show', conditions=dict(method=['GET']), ckan_icon='question-sign')
        map.connect('suggest_view', '/%s/view/{id}' % constants.SUGGESTS_MAIN_PATH,
                  controller='ckanext.ksext.controllers.Suggest:SuggestsController',
                  action='views', conditions=dict(method=['GET','POST']), ckan_icon='question-sign')
       # Comment, update and view comments (of) a Data Request
        map.connect('suggest_comment', '/%s/{id}/comment' % constants.SUGGESTS_MAIN_PATH,
                  controller='ckanext.ksext.controllers.Suggest:SuggestsController',
                  action='suggest_comment', conditions=dict(method=['GET', 'POST']), ckan_icon='comment')

        map.connect('suggest_domail', '/%s/domail/{id}' % constants.SUGGESTS_MAIN_PATH,
                  controller='ckanext.ksext.controllers.Suggest:SuggestsController',
                  action='domail', conditions=dict(method=['GET','POST']), ckan_icon='question-sign')

    	return map

    def before_map(self, map):
        
        return map

    def get_helpers(self):
        return {
            'ksexthots': ksext_hots
        } 
