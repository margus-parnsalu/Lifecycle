"""
Core actions for Service Layer Pattern
Modules implement actions in actions.py files.
"""
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound
from paginate_sqlalchemy import SqlalchemyOrmPage

from abc import ABCMeta

from .models import DBSession
from .utils.sorts import SortValue
from .utils.filters import sqla_dyn_filters


class CoreError(Exception):
    def __init__(self, msg):
        self.msg = msg


class SortError(CoreError):
    def __init__(self, msg='Sort value not found!'):
        self.msg = msg


class DBError(DBAPIError):
    def __init__(self, msg='DB connection error!'):
        self.msg = msg


class NoResultError(NoResultFound):
    def __init__(self, msg='Resource not found!'):
        self.msg = msg


class BaseAction(object):
    __metaclass__ = ABCMeta

    __model__ = None
    __DBSession__ = DBSession

    def __init__(self, filters=None, sort=None, limit=None, page=None):
        self.sort = sort
        self.page = page
        self.limit = limit
        self.filter = filters
        self.query = self.base_query()

    def run_query(self):
        # Filter
        if self.filter:
            self.query = self.filtering()
        # Sorting
        reverse_sort = None
        if self.sort:
            sort, reverse_sort = self.sorting()
            self.query = self.query.order_by(text(sort))
        # Limit
        if self.limit:
            self.query = self.query.limit(self.limit)
        # Paging
        if self.page:
            self.query = self.paging(self.query)

        query = self.query
        if not query:
            raise NoResultError()
        return query, reverse_sort

    def sorting(self):
        # Sorting custom code from sorts.py
        sort = SortValue(self.sort)
        sort_value = sort.sort_str()
        if sort_value == '':
            raise SortError()
        return sort_value, sort.reverse_direction()

    def paging(self, query):
        return (SqlalchemyOrmPage(query,
                                  page=self.page['current_page'],
                                  url_maker=self.page['url_for_page'],
                                  items_per_page=self.page['items_per_page']))

    def filtering(self):
        return sqla_dyn_filters(self.filter, self.query, self.__model__)

    def get_by_pk(self, pk):
        query = self.__DBSession__.query(self.__model__).get(pk)
        if not query:
            raise NoResultError()
        return query

    def base_query(self):
        """Simple model base query for building extensions"""
        return self.__DBSession__.query(self.__model__)

    def db_load(self, modelobj):
        """Supports insert, update into DB"""
        return self.__DBSession__.add(modelobj)

    def add_form_model(self, form):
        """Maps form object fields and data against Model class. Returns Model instance"""
        kvmap = {}
        for field, value in form.data.items():
            if hasattr(self.__model__, field):  # validate
                kvmap[field] = value
            else:
                raise CoreError('Missing attribute in model.')
        return self.__model__(**kvmap)  # new model

    def edit_form_model(self, model, form):
        """Updates model instace attribute values from form"""
        for field, value in form.data.items():
            if hasattr(model, field):  # validate
                setattr(model, field, value)
            else:
                raise CoreError('Missing attribute in model.')
        return model
