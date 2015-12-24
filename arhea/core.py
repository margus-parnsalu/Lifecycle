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

    def __init__(self, filter=None, extd_filter=None, sort=None, limit=None, page=None):
        self.sort = sort
        self.page = page
        self.limit = limit
        self.filter = filter  # Filter dict
        self.extd_filter = extd_filter  # Dict list key=validation class, value=filter dict
        self.query = self.base_query()

    def base_query(self):
        """Simple model base query for building extensions"""
        return self.__DBSession__.query(self.__model__)

    def run_query(self):
        # Filter
        if self.filter:
            self.crud_filtering()
        if self.extd_filter:
            self.extended_filtering()
        # Sorting
        reverse_sort = None
        if self.sort:
            sort, reverse_sort = self.sorting()
            self.query = self.query.order_by(text(sort))
            self.reverse_sort = reverse_sort
        # Limit
        if self.limit:
            self.query = self.query.limit(self.limit)
        # Paging
        if self.page: # SqlAlchemyORMPaging object is created
            self.query = self.paging(self.query)
            query = self.query
        else: # If no paging then query all.
            query = self.query.all()

        if not query:
            raise NoResultError()
        return query

    def sorting(self):
        """Sorting custom code from sorts.py"""
        sort = SortValue(self.sort)
        sort_value = sort.sort_str()
        if sort_value == '':
            raise SortError()
        return sort_value, sort.reverse_direction()

    def paging(self, query):
        """Creating paging response object with records"""
        return (SqlalchemyOrmPage(query,
                                  page=self.page['current_page'],
                                  url_maker=self.page['url_for_page'],
                                  items_per_page=self.page['items_per_page']))

    def crud_filtering(self):
        """Based on filter dict extend query object. Validation based on self __model__ class"""
        for attr, value in self.filter.items():
            if value == '':
                value = '%'
            try:
                self.query = (self.query.filter(getattr(self.__model__, attr).
                                                    ilike(value)))
            except:
                pass  # When model object does not have dictionary value do nothing

    def extended_filtering(self):
        """Based on validation class and filter dict list extend query object"""
        for validation_class, filter in self.extd_filter.items():
            for attr, value in filter.items():
                if value == '':
                    value = '%'
                try:
                    self.query = (self.query.filter(getattr(validation_class, attr).
                                                        ilike(value)))
                except:
                    pass  # When model object does not have dictionary value do nothing

    @classmethod
    def get_by_pk(cls, pk):
        query = cls.__DBSession__.query(cls.__model__).get(pk)
        if not query:
            raise NoResultError()
        return query

    @classmethod
    def create_model_object(cls, data):
        """Maps  data against Model class. Returns Model instance"""
        kvmap = {}
        #import pdb; pdb.set_trace()
        for key, value in data.items():
            if hasattr(cls.__model__, key):  # validate
                kvmap[key] = value
            else:
                pass
        return cls.__model__(**kvmap)  # new model

    @staticmethod
    def update_model_object(object, data):
        """Updates model instace attribute values from form"""
        for key, value in data.items():
            if hasattr(object, key):  # validate
                setattr(object, key, value)
            else:
                #raise CoreError('Missing attribute in model.')
                pass
        return object

    @classmethod
    def db_load(cls, modelobj):
        """Supports insert, update into DB"""
        return cls.__DBSession__.add(modelobj)
