"""
General application views
"""
from pyramid.view import view_config
from pyramid.security import authenticated_userid

import logging
log = logging.getLogger(__name__)



@view_config(route_name='home', renderer='home.jinja2', request_method='GET', permission='view')
def home(request):
    """Homepage view"""
    project_name = 'Telekom rakenduste ja vastutajate nimekiri_'

    #Logging example
    #log.info('Returning project name: %s', project_name)

    #Python debugger for troubleshooting
    #import pdb; pdb.set_trace()

    return {'project': project_name,
            'logged_in': request.authenticated_userid}











