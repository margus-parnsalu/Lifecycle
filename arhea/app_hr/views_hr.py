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
from ..app_util.sorts import SortValue
from ..models import (DBSession, ITEMS_PER_PAGE, conn_err_msg)
from .forms_hr import (DepartmentForm, EmployeeForm)
from .models_hr import (Department, Employee)



@view_config(route_name='department_view', renderer='department_r.jinja2',
             request_method='GET', permission='view')
@view_config(route_name='department_view:page', renderer='department_r.jinja2',
             request_method='GET', permission='view')
def department_view(request):

    sort_input = request.GET.get('sort', '+department')
    #Sorting custom code from sorts.py
    sort = SortValue(sort_input)
    sort_value = sort.sort_str()
    if sort_value == '':
        return HTTPFound(location=request.route_url('home'))
    sort_dir = sort.reverse_direction()

    #SqlAlchemy query object for the report
    departments = DBSession.query(Department).order_by(text(sort_value))

    #Pagination logic with Sqlalchemy object
    current_page = int(request.matchdict.get('page', '1'))
    url_for_page = lambda p: request.route_url('department_view:page', page=p,
                                               _query=(('sort', sort_input), ))
    try:
        records = SqlalchemyOrmPage(departments, current_page,
                                    url_maker=url_for_page, items_per_page=ITEMS_PER_PAGE)
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'departments': records,
            'sortdir': sort_dir,
            'logged_in': authenticated_userid(request)}



@view_config(route_name='department_add', renderer='department_f.jinja2',
             request_method=['GET', 'POST'], permission='edit')
def department_add(request):

    form = DepartmentForm(request.POST, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        dep = Department(department_name=form.department_name.data)
        DBSession.add(dep)
        request.session.flash('Department Added!')
        return HTTPFound(location=request.route_url('department_view'))

    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='department_edit', renderer='department_f.jinja2',
             request_method=['GET', 'POST'], permission='edit')
def department_edit(request):

    try:
        department = (DBSession.query(Department).
                      filter(Department.department_id == request.matchdict['dep_id']).one())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    except NoResultFound:
        return HTTPNotFound('Department not found!')

    form = DepartmentForm(request.POST, department, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        department.department_name = form.department_name.data
        DBSession.add(department)
        request.session.flash('Department Updated!')
        return HTTPFound(location=request.route_url('department_view'))

    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='employee_view', renderer='employee_r.jinja2',
             request_method='GET', permission='view')
@view_config(route_name='employee_view:page', renderer='employee_r.jinja2',
             request_method='GET', permission='view')
def employee_view(request):

    sort_input = request.GET.get('sort', '+employee')
    #Sorting custom code from sorts.py
    sort = SortValue(sort_input)
    sort_value = sort.sort_str()
    if sort_value == '':
        return HTTPFound(location=request.route_url('home'))
    sort_dir = sort.reverse_direction()

    #SqlAlchemy query object
    employees = (DBSession.query(Employee, Department).
                 outerjoin(Department, Employee.department_id == Department.department_id).
                 filter(Employee.end_date == None).
                 order_by(text(sort_value)))


    #Pagination logic
    current_page = int(request.matchdict.get('page', '1'))
    url_for_page = lambda p: request.route_url('employee_view:page', page=p,
                                               _query=(('sort', sort_input), ))
    try:
        records = (SqlalchemyOrmPage(employees, current_page, url_maker=url_for_page,
                                     items_per_page=ITEMS_PER_PAGE))
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'employees': records,
            'sortdir': sort_dir,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='employee_add', renderer='employee_f.jinja2',
             request_method=['GET', 'POST'], permission='edit')
def employee_add(request):

    form = EmployeeForm(request.POST, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        emp = Employee(first_name=form.first_name.data,
                       last_name=form.last_name.data,
                       email=form.email.data,
                       phone_number=form.phone_number.data,
                       salary=form.salary.data,
                       hire_date=form.hire_date.data,
                       end_date=form.end_date.data,
                       department=form.department.data)
        DBSession.add(emp)
        request.session.flash('Employee Added!')
        return HTTPFound(location=request.route_url('employee_view'))

    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='employee_edit', renderer='employee_f.jinja2',
             request_method=['GET', 'POST'], permission='edit')
def employee_edit(request):

    try:
        employee = (DBSession.query(Employee).
                    filter(Employee.employee_id == request.matchdict['emp_id']).one())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    except NoResultFound:
        return HTTPNotFound('Employee not found!')


    form = EmployeeForm(request.POST, employee, csrf_context=request.session)

    if request.method == 'POST' and form.validate():
        #Update Employee
        employee.first_name = form.first_name.data
        employee.last_name = form.last_name.data
        employee.email = form.email.data
        employee.phone_number = form.phone_number.data
        employee.salary = form.salary.data
        employee.hire_date = form.hire_date.data
        employee.department = form.department.data
        employee.end_date = form.end_date.data
        DBSession.add(employee)
        request.session.flash('Employee Updated!')
        return HTTPFound(location=request.route_url('employee_view'))

    return {'form': form,
            'logged_in': authenticated_userid(request)}
