"""
HR Views
"""
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import text

#SqlAlchemy object pagination logic extends Paginate
from paginate_sqlalchemy import SqlalchemyOrmPage

#Sorting logic
from ..utils.sorts import SortValue
from ..utils.filters import sqla_dyn_filters, req_get_todict, req_paging_dict
from ..models import (DBSession, ITEMS_PER_PAGE, conn_err_msg)
from .forms_hr import (DepartmentForm, EmployeeForm)
from .models_hr import (Department, Employee)
from .actions import DepartmentAction, EmployeeAction, SortError, DBError, NoResultError

from cornice.resource import resource

from marshmallow import Schema, fields, ValidationError, pre_load

class DepartmentSchema(Schema):
    department_id = fields.Int(dump_only=True)
    department_name = fields.Str()
    formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, dep):
        return "{}-{}".format(dep.department_id, dep.department_name)

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)


#departments = Service(name='Departments', path='/api/departments/{dep}', description="Cornice Demo")

@resource(collection_path='/api/departments', path='/api/departments/{id:\d+}')
class DepartmentResource(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        departments = DBSession.query(Department).all()
        result = departments_schema.dump(departments)
        return {'departments': result.data}

    def get(self):
        department = DBSession.query(Department).get(self.request.matchdict['id'])
        #import pdb; pdb.set_trace()
        result = department_schema.dump(department)
        return {'departments': result.data}

    def collection_post(self):
        # curl -H "Content-Type: application/json" -X POST -d '{"department_name":"cornice"}' http://localhost:6544/api/departments

        data, errors = department_schema.load(self.request.json)
        if errors:
            return errors
        dep = Department(department_name=data['department_name'])
        DBSession.add(dep)
        return {'department': self.request.json}

    def put(self):
        # curl -H "Content-Type: application/json" -X PUT -d '{"department_name":"PUT"}' http://localhost:6544/api/departments/1

        data, errors = department_schema.load(self.request.json)
        if errors:
            return errors
        try:
            department = (DBSession.query(Department).get(self.request.matchdict['id']))
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)
        if not department:
            raise Exception('Department not found!')
        department.department_name=data['department_name']
        DBSession.add(department)
        return {'department': self.request.json}


@view_config(route_name='department_view', renderer='department_r.jinja2',
             request_method='GET', permission='view')
@view_config(route_name='department_view:page', renderer='department_r.jinja2',
             request_method='GET', permission='view')
def department_view(request):

    sort_input = request.GET.get('sort', '+department')
    paging_input = req_paging_dict(request, sort_input, ITEMS_PER_PAGE)

    try:
        departments, reverse_sort = DepartmentAction(filter=request.GET.items(),
                                                     sort=sort_input,
                                                     page=paging_input).get_departments()
    except SortError:
        return HTTPFound(location=request.route_url('home'))
    except NoResultError:
        return HTTPNotFound('Resource not found!')


    return {'records': departments,
            'sortdir': reverse_sort,
            'query': req_get_todict(request.GET),
            'logged_in': request.authenticated_userid}



@view_config(route_name='department_add', renderer='department_f.jinja2',
             request_method=['GET', 'POST'], permission='view')
def department_add(request):

    form = DepartmentForm(request.POST, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        #dep = Department(department_name=form.department_name.data)
        #DBSession.add(dep)
        DepartmentAction().add_department(form=form)
        #import pdb; pdb.set_trace()
        request.session.flash('Department Added!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('department_view'))

    return {'form': form,
            'logged_in': request.authenticated_userid}


@view_config(route_name='department_edit', renderer='department_f.jinja2',
             request_method=['GET', 'POST'], permission='view')
def department_edit(request):

    try:
        department = DepartmentAction().get_department(request.matchdict['dep_id'])
    except SortError:
        return HTTPFound(location=request.route_url('home'))
    except NoResultError:
        return HTTPNotFound('Resource not found!')

    form = DepartmentForm(request.POST, department, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        DepartmentAction().edit_department(department, form)
        request.session.flash('Department Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('department_view'))

    return {'form': form,
            'logged_in': request.authenticated_userid}


@view_config(route_name='employee_view', renderer='employee_r.jinja2',
             request_method='GET', permission='view')
@view_config(route_name='employee_view:page', renderer='employee_r.jinja2',
             request_method='GET', permission='view')
def employee_view(request):

    sort_input = request.GET.get('sort', '+employee')
    paging_input = req_paging_dict(request, sort_input, 3)

    try:
        employees, reverse_sort = EmployeeAction(sort=sort_input, page=paging_input).get_employees()
    except SortError:
        return HTTPFound(location=request.route_url('home'))

    return {'records': employees,
            'sortdir': reverse_sort,
            'query': req_get_todict(request.GET),
            'logged_in': request.authenticated_userid}


@view_config(route_name='employee_add', renderer='employee_f.jinja2',
             request_method=['GET', 'POST'], permission='view')
def employee_add(request):

    form = EmployeeForm(request.POST, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        EmployeeAction().add_employee(form=form)
        request.session.flash('Employee Added!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('employee_view'))

    return {'form': form,
            'logged_in': request.authenticated_userid}


@view_config(route_name='employee_edit', renderer='employee_f.jinja2',
             request_method=['GET', 'POST'], permission='view')
def employee_edit(request):

    try:
        employee = EmployeeAction().get_employee(request.matchdict['emp_id'])
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    except NoResultFound:
        return HTTPNotFound('Employee not found!')


    form = EmployeeForm(request.POST, employee, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        #Update Employee
        DepartmentAction().edit_department(employee, form)
        request.session.flash('Employee Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('employee_view'))

    return {'form': form,
            'logged_in': request.authenticated_userid}
