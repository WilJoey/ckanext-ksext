import ckan.plugins as p
#from ckan.lib.base import BaseController, config
import ckan.lib.base as base
import ckan.lib.helpers as h
import ckan.model as model
import ckan.logic as logic
import ckan.logic.schema as schema
import ckan.new_authz as new_authz
import ckan.lib.captcha as captcha
import ckan.lib.navl.dictization_functions as dictization_functions
from pylons import config
from ckan.common import _, c, g, request

c = base.c
request = base.request


class MUserController(base.BaseController):
    
    def index (self):
        LIMIT = 20

        page = int(request.params.get('page', 1))
        c.q = request.params.get('q', '')
        c.order_by = request.params.get('order_by', 'name')

        context = {'return_query': True, 'user': c.user or c.author,
                   'auth_user_obj': c.userobj}

        data_dict = {'q': c.q,
                     'limit': LIMIT,
                     'offset': (page - 1) * LIMIT,
                     'order_by': c.order_by}
        try:
            logic.check_access('user_list', context, data_dict)
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))

        users_list = logic.get_action('user_list')(context, data_dict)
        c.users = users_list

        c.page = h.Page(
            collection=users_list,
            page=page,
            url=h.pager_url,
            item_count=users_list.count(),
            items_per_page=LIMIT
        )
        return base.render('muser/index.html')
        

    def new (self, data=None, errors=None, error_summary=None):
        #q = model.Session.query(model.User).filter(model.User.sysadmin==True)
        #c.sysadmins = [a.name for a in q.all()]

        '''GET to display a form for registering a new user.
           or POST the form data to actually do the user registration.
        '''
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author,
                   'auth_user_obj': c.userobj,
                   'schema': self._new_form_to_db_schema(),
                   'save': 'save' in request.params}
        c.is_sysadmin = new_authz.is_sysadmin(c.user)
        if not c.user or not c.is_sysadmin:
            return base.render('user/logout_first.html')

        try:
            logic.check_access('user_create', context)
        except logic.NotAuthorized:
            base.abort(401, _('Unauthorized to create a user'))

        if context['save'] and not data:
            return self._save_new(context)

        c.data = data or {}
        c.errors = errors or {}
        c.error_summary = error_summary or {}
        #vars = {'data': data, 'errors': errors, 'error_summary': error_summary}


        #c.form = render(self.new_user_form, extra_vars=vars)
        #return render('user/new.html')

        return base.render('muser/new.html')

    def _new_form_to_db_schema(self):
        return schema.user_new_form_schema()
    
    def _save_new(self, context):
        try:
            data_dict = logic.clean_dict(dictization_functions.unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')
            captcha.check_recaptcha(request)
            user = logic.get_action('user_create')(context, data_dict)
        except logic.NotAuthorized:
            base.abort(401, _('Unauthorized to create user %s') % '')
        except logic.NotFound, e:
            base.abort(404, _('User not found'))
        except dictization_functions.DataError:
            base.abort(400, _(u'Integrity Error'))
        except captcha.CaptchaError:
            error_msg = _(u'Bad Captcha. Please try again.')
            h.flash_error(error_msg)
            return self.new(data_dict)
        except logic.ValidationError, e:
            c.errors = e.error_dict
            c.error_summary = e.error_summary
            return self.new(data_dict, c.errors, c.error_summary)

        # success
        h.flash_success(_('User "%s" is now registered.') % (data_dict['name']))
        #return base.render('user/logout_first.html')
        return base.render('muser/new.html')

    def edit(self, id=None, data=None, errors=None, error_summary=None):
        context = {'save': 'save' in request.params,
                   'schema': self._edit_form_to_db_schema(),
                   'model': model, 'session': model.Session,
                   'user': c.user, 'auth_user_obj': c.userobj
                   }
        if id is None:
            base.abort(400, _('No user specified'))

        if not new_authz.is_sysadmin(c.user):
            base.abort(401, _('User %s not authorized to edit %s') % (str(c.user), id))

        data_dict = {'id': id}

        try:
            logic.check_access('user_update', context, data_dict)
        except logic.NotAuthorized:
            base.abort(401, _('Unauthorized to edit a user.'))

        if (context['save']) and not data:
            return self._save_edit(id, context)

        try:
            old_data = logic.get_action('user_show')(context, data_dict)

            schema = self._db_to_edit_form_schema()
            if schema:
                old_data, errors = validate(old_data, schema)

            c.display_name = old_data.get('display_name')
            c.user_name = old_data.get('name')

            data = data or old_data

        except logic.NotAuthorized:
            base.abort(401, _('Unauthorized to edit user %s') % '')
        except logic.NotFound:
            base.abort(404, _('User not found'))

        user_obj = context.get('user_obj')

        errors = errors or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}

        self._setup_template_variables({'model': model,
                                        'session': model.Session,
                                        'user': c.user or c.author},
                                       data_dict)

        c.is_myself = True
        c.show_email_notifications = h.asbool(
            config.get('ckan.activity_streams_email_notifications'))
        c.form = base.render('muser/edit_user_form.html', extra_vars=vars)

        return base.render('muser/edit.html')

    def _save_edit(self, id, context):
        try:
            data_dict = logic.clean_dict(dictization_functions.unflatten(
                logic.tuplize_dict(logic.parse_params(request.params))))
            context['message'] = data_dict.get('log_message', '')
            data_dict['id'] = id

            # MOAN: Do I really have to do this here?
            if 'activity_streams_email_notifications' not in data_dict:
                data_dict['activity_streams_email_notifications'] = False

            user = logic.get_action('user_update')(context, data_dict)
            
            h.flash_success(_('Profile updated'))
            user_index = h.url_for(controller='ckanext.ksext.controllers.MUser:MUserController', action='index')
            h.redirect_to(user_index)

            
        except logic.NotAuthorized:
            base.abort(401, _('Unauthorized to edit user %s') % id)
        except logic.NotFound, e:
            base.abort(404, _('User not found'))
        except dictization_functions.DataError:
            base.abort(400, _(u'Integrity Error'))
        except logic.ValidationError, e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.edit(id, data_dict, errors, error_summary)

    def _setup_template_variables(self, context, data_dict):
        c.is_sysadmin = new_authz.is_sysadmin(c.user)
        try:
            user_dict = logic.get_action('user_show')(context, data_dict)
        except logic.NotFound:
            base.abort(404, _('User not found'))
        except logic.NotAuthorized:
            base.abort(401, _('Not authorized to see this page'))
        c.user_dict = user_dict
        c.is_myself = user_dict['name'] == c.user
        c.about_formatted = h.render_markdown(user_dict['about'])

    def _db_to_edit_form_schema(self):
        '''This is an interface to manipulate data from the database
        into a format suitable for the form (optional)'''

    def _edit_form_to_db_schema(self):
        return schema.user_edit_form_schema()

    def delete(self, id):
        '''Delete user with id passed as parameter'''
        context = {'model': model,
                   'session': model.Session,
                   'user': c.user,
                   'auth_user_obj': c.userobj}
        data_dict = {'id': id}

        try:
            logic.get_action('user_delete')(context, data_dict)
            h.flash_success(_('User deleted!'))
            user_index = h.url_for(controller='ckanext.ksext.controllers.MUser:MUserController', action='index')
            h.redirect_to(user_index)
        except logic.NotAuthorized:
            msg = _('Unauthorized to delete user with id "{user_id}".')
            base.abort(401, msg.format(user_id=id))


