"""
SD  package views
"""
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
import requests
import json

from ..utils.utils import req_get_todict
from .actions import CIAction


@view_config(route_name='ci_load_view', renderer='json',
             request_method='GET', permission='admin')
def ci_load_view(request):

    host = request.registry.settings['sd.host']
    user = request.registry.settings['sd.user']
    pwd = request.registry.settings['sd.pwd']

    CIAction.replicate_ci(user, pwd, host)

    return HTTPFound(location=request.route_url('ci_codes_view'))


@view_config(route_name='ci_codes_view', renderer='sdci_r.jinja2',
             request_method='GET', permission='view')
def ci_codes_view(request):


    sort_input = request.GET.get('sort', '+name')

    sdci_act = CIAction(sort=sort_input)

    sdci = sdci_act.get_internal_cis()



    return {'sdcis': sdci,
            'query': req_get_todict(request.GET),
            'sortdir': sdci_act.reverse_sort,
            'logged_in': request.authenticated_userid}


@view_config(route_name='ci_admin_view', renderer='sdci_admin_f.jinja2',
             request_method='GET', permission='admin')
def ci_admin_view(request):

    #sdci = CIAction.get_internal_cis()

    return {'sdcis': 'test',
            'logged_in': request.authenticated_userid}


@view_config(route_name='ci_clean_view',
             request_method='GET', permission='admin')
def ci_clean_view(request):

    CIAction.purge()  # Clean db from CI-s.

    return HTTPFound(location=request.route_url('ci_codes_view'))
