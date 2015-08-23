"""
General application views
"""
from pyramid.view import view_config
from pyramid.security import authenticated_userid


@view_config(route_name='home', renderer='home.jinja2', request_method='GET', permission='view')
def home(request):
    """Homepage view"""
    project_name = 'Applications'
    #Python debugger for troubleshooting
    #import pdb; pdb.set_trace()
    return {'project': project_name,
            'logged_in': authenticated_userid(request)}











