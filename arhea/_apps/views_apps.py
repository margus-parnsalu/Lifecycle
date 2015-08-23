"""
Apps package views
"""
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import subqueryload

from ..models import (DBSession_EA, conn_err_msg)
from ..util.sorts import SortValue
from .forms_apps import (ApplicationForm)
from .models_apps import (TObject, TPackage)

@view_config(route_name='application_view', renderer='application_r.jinja2',
             request_method='GET', permission='view')
def application_view(request):
    #Search form
    form = ApplicationForm(request.GET)

    sort_input = request.GET.get('sort', '+application')
    #Sorting custom code from sorts.py
    sort = SortValue(sort_input)
    sort_value = sort.sort_str()
    if sort_value == '':
        return HTTPFound(location=request.route_url('home'))
    sort_dir = sort.reverse_direction()

    #Handling search Form get parameter passing to template
    if len(request.GET) == 0:#No GET parameters
        query_input = {}
    else:
        #Need to pass GET parameters in dict for route_url
        query_input = {k:v for k, v in request.GET.items()}

    #SqlAlchemy query object
    app_q = (DBSession_EA.query(TObject).
             options(subqueryload('properties')).
             outerjoin(TObject.properties, aliased=True).
             outerjoin(TObject.packages, aliased=True).
             filter(TObject.object_type == 'Package').
             filter(TObject.stereotype.like('system%')).
             filter(TPackage.parent_id.in_([74, 9054])))
    #Dynamically add search filters to query object
    for attr, value in request.GET.items():
        if value == '':
            value = '%'
        try:
            app_q = app_q.filter(coalesce(getattr(TObject, attr), '').like(value))
        except:
            pass#When model object does not have request.GET value do nothing
    #Fetch records from database
    try:
        applications = app_q.order_by(text(sort_value)).limit(1000)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'applications': applications,
            'form': form,
            'query': query_input,
            'sortdir': sort_dir,
            'logged_in': authenticated_userid(request)}
