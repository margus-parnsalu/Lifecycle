"""
SD_apps actions module. Extends BaseAction from core.
"""
from sqlalchemy.orm import subqueryload, load_only
from sqlalchemy import func
from sqlalchemy.sql import label

from ..actions import BaseAction
from ..models import DBSession

from .models import CI


class CIAction(BaseAction):
    __model__ = CI
    __DBSession__ = DBSession


    @classmethod
    def create_ci(cls, data):
        ci = cls.create_model_object(data)
        return cls.db_load(ci)

    @classmethod
    def get_tag(cls, pk):
        return cls.get_by_pk(pk)

    @classmethod
    def edit_ci(cls, obj, data):
        ci = cls.update_model_object(obj, data)
        return cls.db_load(ci)

    @classmethod
    def get_cis(cls):
        return cls.base_query().all()

    @classmethod
    def purge(cls):
        return cls.__DBSession__.query(cls.__model__).delete()

    def get_internal_cis(self):
        self.query = (self.__DBSession__.query(self.__model__).
                     filter(self.__model__.owner.in_(['ELION', 'TELIAEESTI', 'EMT'])).
                     filter(self.__model__.code.like('%-LIVE')))
        return  self.run_query()