"""
Apps package views
"""
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import subqueryload, load_only
from sqlalchemy.orm.exc import NoResultFound

import re
from ..core import SortError, NoResultError, DBError
from .actions import AppsAction
from ..models import (DBSession_EA, conn_err_msg)
from ..utils.sorts import SortValue
from ..utils.filters import sqla_dyn_filters, req_get_todict, req_paging_dict
from .forms_apps import (ApplicationForm, TagUpdateForm, ApplicationTagForm)
from .models_apps import (TObject, TPackage, TObjectproperty, languages_lov)


@view_config(route_name='application_view', renderer='application_r.jinja2',
             request_method='GET', permission='view')
def application_view(request):
    #Search form
    form = ApplicationForm(request.GET, csrf_context=request.session)
    form.gentype.choices = [("", 'Language'), ("", '------')] + languages_lov()

    sort_input = request.GET.get('sort', '+application')

    try:
        applications, reverse_sort = AppsAction(filters=request.GET.items(),
                                                sort=sort_input,
                                                limit=1000).get_applications()
    except SortError:
        return HTTPFound(location=request.route_url('home'))
    except NoResultError:
        return HTTPNotFound('Resource not found!')
    except DBError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'applications': applications,
            'form': form,
            'query': req_get_todict(request.GET),
            'sortdir': reverse_sort,
            'logged_in': request.authenticated_userid}


@view_config(route_name='tag_edit', renderer='tag_f.jinja2',
             request_method=['GET', 'POST'], permission='edit_tag')
def tag_edit(request):

    try:
        tag_property = (DBSession_EA.query(TObjectproperty).
                        filter(TObjectproperty.propertyid == request.matchdict['tag_id']).one())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    except NoResultFound:
        return HTTPNotFound('Tag not found!')

    form = TagUpdateForm(request.POST, tag_property, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        tag_property.value = form.value.data
        DBSession_EA.add(tag_property)
        request.session.flash('Tag Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('application_view',
                                                    _anchor=request.GET.get('app', '')))

    return {'form': form,
            'app_name': request.GET.get('app', ''),
            'logged_in': request.authenticated_userid}


@view_config(route_name='app_tags_edit', renderer='app_tags_f.jinja2',
             request_method=['GET', 'POST'], permission='edit_app')
def app_tags_edit(request):

    try:
        app = (DBSession_EA.query(TObject).
                    filter(TObject.object_id == request.matchdict['app_id']).one())
        tags = (DBSession_EA.query(TObjectproperty).
               filter(TObjectproperty.object_id == request.matchdict['app_id']).all())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    except NoResultFound:
        return HTTPNotFound('Application not found!')

    form = ApplicationTagForm(request.POST, app=app, tags=tags, csrf_context=request.session)
    form.app.gentype.choices = languages_lov()

    if request.method == 'POST' and form.validate():
        #Tags
        for field_set in form.tags.entries:
            if field_set.value.data:
                #Find fieldset number to match query object
                match = re.search(r'\d', field_set.property.name)
                i = int(match.group())
                tags[i].value = field_set.value.data
                DBSession_EA.add(tags[i])
        #App
        app.name = form.app['name'].data
        app.alias = form.app.alias.data
        app.status = form.app.status.data
        app.stereotype = form.app.stereotype.data
        app.gentype = form.app.gentype.data
        app.note = form.app.note.data
        DBSession_EA.add(app)
        request.session.flash('Application information Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('application_view',
                                                    _anchor=request.GET.get('app', '')))

    return {'form': form,
            'app_name': request.GET.get('app', ''),
            'logged_in': request.authenticated_userid}