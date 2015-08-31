"""
Apps package views
"""
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import subqueryload, load_only
from sqlalchemy.orm.exc import NoResultFound

from ..models import (DBSession_EA, conn_err_msg)
from ..utils.sorts import SortValue
from ..utils.filters import sqla_dyn_filters, req_get_todict
from .forms_apps import (ApplicationForm, TagUpdateForm)
from .models_apps import (TObject, TPackage, TObjectproperty)


@view_config(route_name='application_view', renderer='application_r.jinja2',
             request_method='GET', permission='view')
def application_view(request):
    #Search form
    form = ApplicationForm(request.GET)

    sort_input = request.GET.get('sort', '+application')
    sort = SortValue(sort_input)
    sort_value = sort.sort_str()
    if sort_value == '':
        return HTTPFound(location=request.route_url('home'))

    #SqlAlchemy query object
    app_q = (DBSession_EA.query(TObject).
             options(subqueryload('properties').load_only("property", "value")).
             options(load_only("name", "alias", "stereotype", "status", "note", "ea_guid")).
             outerjoin(TObject.properties, aliased=True).
             outerjoin(TObject.packages, aliased=True).
             filter(TObject.object_type == 'Package').
             filter(TObject.stereotype.like('system%')).
             filter(TPackage.parent_id.in_([74, 9054])))

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
            'logged_in': authenticated_userid(request)}


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
            'logged_in': authenticated_userid(request)}