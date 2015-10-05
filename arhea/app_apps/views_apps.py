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
from ..models import (DBSession_EA, conn_err_msg)
from ..utils.sorts import SortValue
from ..utils.filters import sqla_dyn_filters, req_get_todict
from .forms_apps import (ApplicationForm, TagUpdateForm, ApplicationTagForm)
from .models_apps import (TObject, TPackage, TObjectproperty)


@view_config(route_name='application_view', renderer='application_r.jinja2',
             request_method='GET', permission='view')
def application_view(request):
    #Search form
    form = ApplicationForm(request.GET, csrf_context=request.session)

    sort_input = request.GET.get('sort', '+application')
    sort = SortValue(sort_input)
    sort_value = sort.sort_str()
    if sort_value == '':
        return HTTPFound(location=request.route_url('home'))

    #SqlAlchemy query object
    app_q = (DBSession_EA.query(TObject).
             options(subqueryload('properties').load_only("property", "value")).
             options(load_only("name", "alias", "stereotype", "status", "note", "ea_guid", "gentype")).
             outerjoin(TObject.properties, aliased=True).
             outerjoin(TObject.packages, aliased=True).
             filter(TObject.object_type == 'Package').
             filter(TObject.stereotype.like('system%')).
             filter(TPackage.parent_id.in_([74, 9054, 9055])))
            #9054 - Systems, 9055 - Service PLatforms
    #Dynamically add search filters to query object
    app_q = sqla_dyn_filters(filter_dict=request.GET.items(),
                             query_object=app_q,
                             validation_class=TObject)

    #Fetch records from database
    try:
        applications = app_q.order_by(text(sort_value)).limit(1000)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'applications': applications,
            'form': form,
            'query': req_get_todict(request.GET),
            'sortdir': sort.reverse_direction(),
            'logged_in': request.authenticated_userid}


@view_config(route_name='tag_edit', renderer='tag_f.jinja2',
             request_method=['GET', 'POST'], permission='edit')
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
             request_method=['GET', 'POST'], permission='admin')
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
        app.note = form.app.note.data
        DBSession_EA.add(app)
        request.session.flash('Application information Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('application_view',
                                                    _anchor=request.GET.get('app', '')))

    return {'form': form,
            'app_name': request.GET.get('app', ''),
            'logged_in': request.authenticated_userid}