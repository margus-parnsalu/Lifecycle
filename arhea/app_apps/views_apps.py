"""
Apps package views
"""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

import re
from .actions import AppsAction, TagsAction
from ..utils.utils import req_get_todict, form_to_dict
from .forms_apps import (ApplicationForm, TagUpdateForm, ApplicationTagForm)
from .models_apps import (languages_lov)


@view_config(route_name='application_view', renderer='application_r.jinja2',
             request_method='GET', permission='view')
def application_view(request):
    sort_input = request.GET.get('sort', '+application')
    #Search form
    form = ApplicationForm(request.GET, csrf_context=request.session)
    form.gentype.choices = [("", 'Language'), ("", '------')] + languages_lov()

    app_act = AppsAction(filter=request.GET, sort=sort_input, limit=1000)
    applications = app_act.get_applications()

    return {'records': applications,
            'form': form,
            'query': req_get_todict(request.GET),
            'sortdir': app_act.reverse_sort,
            'logged_in': request.authenticated_userid}


@view_config(route_name='tag_edit', renderer='tag_f.jinja2',
             request_method=['GET', 'POST'], permission='edit_tag')
def tag_edit(request):

    tag_property = TagsAction.get_tag(request.matchdict['tag_id'])

    form = TagUpdateForm(request.POST, tag_property, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        TagsAction.edit_tag(object=tag_property, data=form_to_dict(form))

        request.session.flash('Tag Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('application_view',
                                                    _anchor=request.GET.get('app', '')))

    return {'form': form,
            'app_name': request.GET.get('app', ''),
            'logged_in': request.authenticated_userid}


@view_config(route_name='app_tags_edit', renderer='app_tags_f.jinja2',
             request_method=['GET', 'POST'], permission='edit_app')
def app_tags_edit(request):

    app_id= request.matchdict['app_id']
    app = AppsAction.get_app(app_id)
    tags = TagsAction.get_app_tags(app_id)

    form = ApplicationTagForm(request.POST, app=app, tags=tags, csrf_context=request.session)
    form.app.gentype.choices = languages_lov()

    if request.method == 'POST' and form.validate():
        #Tags
        for field_set in form.tags.entries:
            if field_set.value.data:
                #Find fieldset number to match query object
                match = re.search(r'\d', field_set.property.name)
                i = int(match.group())

                TagsAction.edit_tag(object=tags[i], data=form_to_dict(field_set))
        #App
        AppsAction.edit_app(object=app, data=form_to_dict(form.app))

        request.session.flash('Application information Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('application_view',
                                                    _anchor=request.GET.get('app', '')))
    return {'form': form,
            'app_name': request.GET.get('app', ''),
            'logged_in': request.authenticated_userid}