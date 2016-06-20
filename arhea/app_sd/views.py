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
    #payload = {'par_id': source_invoice_id}
    r = requests.get(host + '/sd_api_new/rest/ci/category/application', auth=(user, pwd))
    if r.status_code == 200:
        #CIAction.purge()  # Clean db from CI-s.
        codes = json.loads(r.content.decode('UTF-8'))
        for code in codes:
            r = requests.get(host + '/sd_api_new/rest/ci/' + code['code'], auth=(user, pwd))
            if r.status_code == 200:
                ci_data = json.loads(r.content.decode('UTF-8'))
                data = {}
                data['code'] = ci_data['code']
                data['system_id'] = ci_data['system_id']
                data['name'] = ci_data['name']
                data['owner'] = ci_data['owner']
                data['remark'] = ci_data['remark']
                data['performer1'] = ci_data['performer1']
                data['performer2'] = ci_data['performer2']
                CIAction.create_ci(data)

                #import pdb; pdb.set_trace()

        return HTTPFound(location=request.route_url('ci_codes_view'))
    else:
        return r.content.decode('UTF-8')


@view_config(route_name='ci_codes_view', renderer='sdci_r.jinja2',
             request_method='GET', permission='view')
def ci_codes_view(request):


    sort_input = request.GET.get('sort', '+name')

    sdci_act = CIAction(sort=sort_input)

    sdci = sdci_act.get_internal_cis()


    return {'sdcis': sdci,
            'query': req_get_todict(request.GET),
            'sortdir': sdci_act.reverse_sort,}


@view_config(route_name='ci_admin_view', renderer='sdci_admin_f.jinja2',
             request_method='GET', permission='admin')
def ci_admin_view(request):

    #sdci = CIAction.get_internal_cis()

    return {'sdcis': 'test'}
