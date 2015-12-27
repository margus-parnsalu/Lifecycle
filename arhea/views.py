"""
General application views
"""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response

from .actions import SortError, NoResultError, DBError

import logging
log = logging.getLogger(__name__)



@view_config(route_name='home', renderer='home.jinja2', request_method='GET', permission='view')
def home(request):
    """Homepage view"""
    project_name = 'Telekom rakenduste ja vastutajate nimekiri.'

    #Logging example
    #log.info('Returning project name: %s', project_name)

    #Python debugger for troubleshooting
    #import pdb; pdb.set_trace()

    return {'project': project_name,
            'logged_in': request.authenticated_userid}


@view_config(context=SortError)
def failed_sort_exception(exc, request):
    """Common handling of Core module exceptions. Sort value not found."""
    return HTTPFound(location=request.route_url('home'))


@view_config(context=NoResultError)
def noresult_query_exception(exc, request):
    """Common handling of Core module exceptions. Query returned no values."""
    return HTTPNotFound(exc.msg)


@view_config(context=DBError)
def dpapi_connection_exception(exc, request):
    """Common handling of Core module exceptions. DBAPI raised exception."""
    return Response(exc.msg, content_type='text/plain', status_int=500)










