# Run tests with Nose and Coverage: nosetests --with-coverage --cover-package=arhea
import unittest
import transaction

from pyramid import testing
from .models_apps import TObject, TObjectproperty, TPackage, TDatatype

def _initTestingDB():
    from sqlalchemy import create_engine
    from ..models import (DBSession_EA, Base_EA)
    from ..app_sec.models_sec import (User, Group)
    import datetime
    import hashlib
    engine = create_engine('sqlite://')
    Base_EA.metadata.create_all(engine)
    DBSession_EA.remove()
    DBSession_EA.configure(bind=engine)
    with transaction.manager:
        #Setup test data
        obj1 = TObject(name='Application', alias='App', stereotype='system', status='Target',
                      note='Test application', ea_guid='{2312083t928njsck}', gentype='Python')
        tag1 = TObjectproperty(object_id=1, property='Architect', value='John Dow')
        tag2 = TObjectproperty(object_id=1, property='Dev domain', value='CRM')
        DBSession_EA.add(obj1)
        DBSession_EA.add(tag1)
        DBSession_EA.add(tag2)

    return DBSession_EA


def _registerRoutes(config):
    config.add_jinja2_search_path('arhea:app_apps/templates')
    #Applications
    config.add_route('application_view', '/apps')
    config.add_route('tag_edit', '/apps/tag/{tag_id:\d+}/edit')
    config.add_route('app_tags_edit', '/apps/{app_id:\d+}/edit')
    # Link to models
    config.add_route('ea_models', 'http://ea.telekom.ee/Telekom/index.html')


class DummyRoute(object):
    """Trick for supporting request.matched_route in case of DummyRequest()"""
    def __init__(self, name):
        self.name = name

from .actions import AppsAction, TagsAction

class AppsActionsTests(unittest.TestCase):
    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_it_get_app(self):
        info = AppsAction.get_app(1)
        self.assertEqual(info.name, 'Application')

    def test_it_edit_app(self):
        data = {'name': 'Test app', 'status': 'Acceptable'}
        app = AppsAction.get_app(1)

        AppsAction.edit_app(app, data)

        info = app #AppsAction.get_app(1)
        self.assertEqual(info.name, 'Test app')
        self.assertEqual(info.status, 'Acceptable')
        self.assertEqual(info.gentype, 'Python')

class TagsActionTests(unittest.TestCase):

    def setUp(self):
        self.session = _initTestingDB()
        self.config = testing.setUp()

    def tearDown(self):
        self.session.remove()
        testing.tearDown()

    def test_it_get_tag(self):
        info = TagsAction.get_tag(1)
        self.assertEqual(info.property, 'Architect')

    def test_it_edit_tag(self):
        tag1_data = {'value': 'Jane Dow'}
        tag2_data = {'value': 'Product'}
        tag1 = TagsAction.get_tag(1)
        tag2 = TagsAction.get_tag(2)

        TagsAction.edit_tag(tag1, tag1_data)
        TagsAction.edit_tag(tag2, tag2_data)

        tag1_info = tag1 #TagsAction.get_tag(1)
        tag2_info = tag2 #TagsAction.get_tag(2)
        self.assertEqual(tag1_info.value, 'Jane Dow')
        self.assertEqual(tag2_info.value, 'Product')

"""
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
"""