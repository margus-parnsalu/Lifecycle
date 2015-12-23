# Run tests with Nose and Coverage: nosetests --with-coverage --cover-package=arhea
import unittest
import transaction

from pyramid import testing
from .models_hr import (Department, Employee)

def _initTestingDB():
    from sqlalchemy import create_engine
    from ..models import (DBSession, Base)
    from ..app_sec.models_sec import (User, Group)
    import datetime
    import hashlib
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    DBSession.remove()
    DBSession.configure(bind=engine)
    with transaction.manager:
        #Setup login information
        grp1 = Group(groupname='Editors')
        usr1 = User(username='editor', pwd=hashlib.sha256(('editor').encode()).hexdigest(),
                    groups=[grp1], start_date=datetime.datetime.now())
        DBSession.add(grp1)
        DBSession.add(usr1)

        #Setup test data
        dep1 = Department(department_name='A Minu Test')
        dep2 = Department(department_name='Z Minu Test')
        DBSession.add(dep1)
        DBSession.add(dep2)
        emp1 = Employee(first_name='John', last_name='Dow', email='john.dow@mail.com',
                        phone_number='879593535', hire_date=datetime.date(2015, 3, 15), salary=3000)
        emp2 = Employee(first_name ='Tom', last_name='Taylor', email='tom.taylor@mail.com',
                        phone_number='87959789', hire_date=datetime.date(2015, 6, 12), salary=5000)
        DBSession.add(emp1)
        DBSession.add(emp2)

    return DBSession


def _registerRoutes(config):
    config.add_route('home', '/')
    config.add_route('department_view', '/departments')
    config.add_route('department_view:page', '/departments/page/{page:\d+}')
    config.add_route('department_add', '/departments/add')
    config.add_route('department_edit', '/departments/{dep_id:\d+}/edit')

    #Employees
    config.add_route('employee_view', '/employees')
    config.add_route('employee_view:page', '/employees/page/{page:\d+}')
    config.add_route('employee_add', '/employees/add')
    config.add_route('employee_edit', '/employees/{emp_id:\d+}/edit')


class DummyRoute(object):
    """Trick for supporting request.matched_route in case of DummyRequest()"""
    def __init__(self, name):
        self.name = name

from .actions import DepartmentAction

class DepartmentActionsTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_it_get_department(self):
        info = DepartmentAction.get_department(1)
        self.assertEqual(info.department_name, 'A Minu Test')

    def test_it_get_departments_no_options(self):
        info = DepartmentAction().get_departments()
        self.assertEqual(len(info), 2)
        self.assertEqual(info[0].department_name, 'A Minu Test')

    def test_it_get_departments_sort(self):
        info = DepartmentAction(sort='-department').get_departments()
        self.assertEqual(len(info), 2)
        self.assertEqual(info[0].department_name, 'Z Minu Test')

    def test_it_get_departments_limit(self):
        info = DepartmentAction(limit=1).get_departments()
        self.assertEqual(len(info), 1)

    def test_it_get_departments_filter(self):
        info = DepartmentAction(filter={'department_name': 'Z%'}).get_departments()
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0].department_name, 'Z Minu Test')

    def test_it_get_departments_filter(self):
        info = DepartmentAction(extd_filter={Department:{'department_name': 'Z%'},
                                             Employee: {'first_name': 'Tom'}}).get_departments()
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0].department_name, 'Z Minu Test')

    def test_it_get_departments_page(self):
        page = {'current_page': 2,
                'url_for_page': lambda p: '/department/page/'+p+'?sort=-department',
                'items_per_page': 1}
        info = DepartmentAction(page=page).get_departments()
        self.assertEqual(len(info), 1)
        self.assertEqual(info[0].department_name, 'Z Minu Test')
        self.assertEqual(info.page_count, 2)
        self.assertEqual(info.items_per_page, 1)

    def test_it_add_department(self):
        data = {'department_name': 'GangOfFour'}
        DepartmentAction.add_department(data)
        info = DepartmentAction.get_department(3)
        self.assertEqual(info.department_name, 'GangOfFour')

    def test_it_edit_department(self):
        data = {'department_name': 'GangOfFour'}
        object = DepartmentAction.get_department(1)
        DepartmentAction.edit_department(object, data)
        info = DepartmentAction.get_department(1)
        self.assertEqual(info.department_name, 'GangOfFour')


class ViewHomeTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from ..views import home
        return home(request)

    def test_it(self):
        _registerRoutes(self.config)
        request = testing.DummyRequest()
        info = self._callFUT(request)
        self.assertEqual(info['project'],
                         """Telekom rakenduste ja vastutajate nimekiri.""")



class ViewDepartmentTests(unittest.TestCase):
    __route__ = 'department_view'

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()
        self.config.testing_securitypolicy(userid='admin',
                                           permissive=True)

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views_hr import department_view
        return department_view(request)

    def test_it(self):
        #from .models import Department
        request = testing.DummyRequest()
        request.matched_route = DummyRoute(self.__route__)

        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['records'][0].department_name, 'A Minu Test')
        self.assertEqual(len(info['records']), 2)

    def test_it_sort_asc(self):
        request = testing.DummyRequest()
        request.matched_route = DummyRoute(self.__route__)
        request.GET['sort'] = '+department'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['records'][0].department_name, 'A Minu Test')
        self.assertEqual(info['records'][1].department_name, 'Z Minu Test')
        self.assertEqual(info['sortdir'], '-')


    def test_it_sort_desc(self):
        request = testing.DummyRequest()
        request.matched_route = DummyRoute(self.__route__)
        request.GET['sort'] = '-department'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['records'][0].department_name, 'Z Minu Test')
        self.assertEqual(info['records'][1].department_name, 'A Minu Test')
        self.assertEqual(info['sortdir'], '+')




class ViewEmployeeTests(unittest.TestCase):
    __route__ = 'employee_view'

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()
        self.config.testing_securitypolicy(userid='admin',
                                           permissive=True)

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def _callFUT(self, request):
        from .views_hr import employee_view
        return employee_view(request)

    def test_it(self):
        request = testing.DummyRequest()
        request.matched_route = DummyRoute(self.__route__)
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['records'][0].Employee.first_name, 'John')
        self.assertEqual(len(info['records']), 2)

    def test_it_sort_asc(self):
        request = testing.DummyRequest()
        request.matched_route = DummyRoute(self.__route__)
        request.GET['sort'] = '+employee'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['records'][0].Employee.first_name, 'John')
        self.assertEqual(info['records'][1].Employee.first_name, 'Tom')
        self.assertEqual(info['sortdir'], '-')


    def test_it_sort_desc(self):
        request = testing.DummyRequest()
        request.matched_route = DummyRoute(self.__route__)
        request.GET['sort'] = '-employee'
        _registerRoutes(self.config)
        info = self._callFUT(request)
        self.assertEqual(info['records'][0].Employee.first_name, 'Tom')
        self.assertEqual(info['records'][1].Employee.first_name, 'John')
        self.assertEqual(info['sortdir'], '+')



class FunctionalTests(unittest.TestCase):

    def setUp(self):
        from arhea.arhea import main
        settings = { 'sqlalchemy.default.url': 'sqlite://',
                     'sqlalchemy.ea.url': 'sqlite://',
                     'jinja2.directories' : ['arhea:arhea/app_sec/templates',
                                             'arhea:arhea/templates',
                                             'arhea:arhea/app_hr/templates',
                                             'arhea:arhea/app_apps/templates'],
                     'session.secret' : 'sess',
                     'auth.secret' : 'auth',
                     'admin_gtwy': 'https://admin-dev.telekom.ee',
                     'ldap.user': 'CN=Arhea,OU=Tehniline,OU=ET,DC=et,DC=ee',
                     'ldap.pwd': 'Pawer5ty9',
                     'ldap.user_base': 'OU=Inimesed,OU=ET,DC=et,DC=ee',
                     'ldap.group_base': 'OU=Arhea,OU=Roll,OU=RBAC,OU=ET,DC=et,DC=ee',

                     }
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

        self.session = _initTestingDB()

        #Login for tests to work
        res = self.testapp.get('/login')
        form = res.form
        form['login'] = 'admin'
        form['password'] = 'changeme'
        form['came_from'] = '/'
        res = form.submit('submit')

    def tearDown(self):
        del self.testapp
        self.session.remove()

    def test_homepage(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'Telekom', res.body)

    def test_unexisting_page(self):
        self.testapp.get('/SomePage', status=404)

    def test_departments_query_sort_unknown(self):
        res = self.testapp.get('/departments?sort=SqlInjection', status=302)
        self.assertEqual(res.location, 'http://localhost/')

    def test_departments_report(self):
        res = self.testapp.get('/departments', status=200)
        self.assertIn(b'<h3>Departments</h3>', res.body)

    def test_employees_report(self):
        res = self.testapp.get('/employees', status=200)
        self.assertIn(b'<h3>Employees</h3>', res.body)

    def test_department_form_add_GET(self):
        # Get the form
        res = self.testapp.get('/departments/add', status=200)
        self.assertIn(b'department_name', res.body)

    def test_department_form_add_POST(self):
        # Get the form
        res = self.testapp.get('/departments/add')
        form = res.form
        form['department_name'] = 'test'
        res = form.submit('submit')
        self.assertEqual(res.location, 'http://localhost/departments')

    def test_department_form_edit_GET(self):
        # Get the form
        res = self.testapp.get('/departments/1/edit', status=200)
        self.assertIn(b'A Minu Test', res.body)

    def test_department_form_edit_GET_unknown_id(self):
        # Get the form
        res = self.testapp.get('/departments/1000/edit', status=404)
        self.assertIn(b'Resource not found!', res.body)

    def test_department_form_edit_POST(self):
        # Get the form
        res = self.testapp.get('/departments/1/edit')
        form = res.form
        form['department_name'] = 'test'
        res = form.submit('submit')
        self.assertEqual(res.location, 'http://localhost/departments')

    def test_employee_form_GET(self):
        # Get the form
        res = self.testapp.get('/employees/add', status=200)
        self.assertIn(b'first_name', res.body)

    def test_employee_form_edit_GET(self):
        # Get the form
        res = self.testapp.get('/employees/1/edit', status=200)
        self.assertIn(b'John', res.body)

    def test_employee_form_edit_GET_unknown_id(self):
        # Get the form
        res = self.testapp.get('/employees/100/edit', status=404)
        self.assertIn(b'Resource not found!', res.body)