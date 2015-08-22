from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.security import authenticated_userid

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import subqueryload
from sqlalchemy import text

#SqlAlchemy object pagination logic extends Paginate
from paginate_sqlalchemy import SqlalchemyOrmPage


from ..models import (DBSession, Department, Employee, ITEMS_PER_PAGE, DBSession_EA,
                     TObject, TPackage, conn_err_msg)
#Sorting logic
from ..sorts import SortValue
from ..forms import (DepartmentForm, EmployeeForm, ApplicationForm)



@view_config(route_name='home', renderer='home.jinja2', request_method='GET', permission='view')
def home(request):
    """Homepage view"""
    project_name = 'Applications'
    #import pdb; pdb.set_trace()
    return {'project': project_name,
            'logged_in': authenticated_userid(request)}



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

    #Debug break point example
    #import pdb; pdb.set_trace()

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
        form.populate_obj(department)
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




