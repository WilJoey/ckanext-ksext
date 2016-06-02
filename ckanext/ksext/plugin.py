<div role="main" class="hero">

    <div class="container" style="height:277px;">
        {% snippet 'home/snippets/search_geo.html' %}
    </div>
</div>

<div role="main">
    <div class="container" style="margin-top:15px;margin-bottom:15px;">
        <div class="row row2">
            <div class="span6 col1">
                {% snippet 'home/snippets/news.html' %}
            </div>
            <div class="span6 col2">
                {% snippet 'home/snippets/stats.html' %}
            </div>

        </div>
    </div>

    <div class="container" style="margin-top:15px;margin-bottom:15px;">
        <div class="row row2">
            <div class="span6 col1">
                {% snippet 'home/snippets/ksext_latest.html' %}
            </div>
            <div class="span6 col2">
                {#% snippet 'home/snippets/featured_organization.html' %#} {% snippet 'home/snippets/ksext_hots.html' %}
            </div>
        </div>
    </div>

</div>


{% resource 'ksext_jscss/js/geo-tips.js' %}    ############################## IACTIONS ##############################
    ######################################################################
    def get_actions(self):
        return {
            'tnstats_dataset_count': a.tnstats_dataset_count,

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
        }

    ######################################################################
    ########################### AUTH FUNCTIONS ###########################
    ######################################################################
    def get_auth_functions(self):
        return {
            constants.SUGGEST_INDEX: auth.suggest_index,
            constants.SUGGEST_CREATE: auth.suggest_create,
            constants.SUGGEST_SHOW: auth.suggest_show,
            # constants.SUGGEST_UPDATE: auth.suggest_update,
            # constants.SUGGEST_DELETE: auth.suggest_delete,
            # constants.SUGGEST_CLOSE: auth.suggest_close,
            constants.SUGGEST_COMMENT: auth.suggest_comment,
            # constants.SUGGEST_COMMENT_LIST: auth.suggest_comment_list,
            # constants.SUGGEST_COMMENT_SHOW: auth.suggest_comment_show,
            constants.SUGGEST_COMMENT_UPDATE: auth.suggest_comment_update,
            # constants.SUGGEST_COMMENT_DELETE: auth.suggest_comment_delete
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

        map.connect('home_show','/show', 
            controller = 'ckanext.ksext.controllers.TnStats:TnStatsController', action='show')
        
        map.connect('home_specification','/specification', 
            controller = 'ckanext.ksext.controllers.TnStats:TnStatsController', action='specification')
        map.connect('home_specification_old','/specification_old',
            controller = 'ckanext.ksext.controllers.TnStats:TnStatsController', action='specification_old')

        map.connect('home_guide','/guide', 
            controller = 'ckanext.ksext.controllers.TnStats:TnStatsController', action='guide')
        map.connect('home_faq','/faq', 
            controller = 'ckanext.ksext.controllers.TnStats:TnStatsController', action='faq')
        map.connect('home_manual','/manual', 
            controller = 'ckanext.ksext.controllers.TnStats:TnStatsController', action='manual')
  
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
                  action='views', conditions=dict(method=['POST']), ckan_icon='question-sign')
       # Comment, update and view comments (of) a Data Request
        map.connect('suggest_comment', '/%s/{id}/comment' % constants.SUGGESTS_MAIN_PATH,
                  controller='ckanext.ksext.controllers.Suggest:SuggestsController',
                  action='suggest_comment', conditions=dict(method=['GET', 'POST']), ckan_icon='comment')

    	return map

    def before_map(self, map):
        
        return map

    def get_helpers(self):
        return {
            'ksexthots': ksext_hots
        } 
