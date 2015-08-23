"""
HR simple demo functionality
__author__ = 'margus'
"""

def include(config):

    #Apps package template location
    config.add_jinja2_search_path('arhea:app_hr/templates')

    #Departments
    config.add_route('department_view', '/departments')
    config.add_route('department_view:page', '/departments/page/{page:\d+}')
    config.add_route('department_add', '/departments/add')
    config.add_route('department_edit', '/departments/{dep_id:\d+}/edit')
    #config.add_route('department_delete', '/departments/{dep_id:\d+}/del')

    #Employees
    config.add_route('employee_view', '/employees')
    config.add_route('employee_view:page', '/employees/page/{page:\d+}')
    config.add_route('employee_add', '/employees/add')
    config.add_route('employee_edit', '/employees/{emp_id:\d+}/edit')