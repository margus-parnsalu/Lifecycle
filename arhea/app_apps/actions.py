"""
App_apps actions module. Extends BaseAction from core.
"""
from sqlalchemy.orm import subqueryload, load_only

from ..actions import BaseAction
from ..models import DBSession_EA

from.models_apps import TObject, TPackage, TObjectproperty


class AppsAction(BaseAction):
    __model__ = TObject
    __DBSession__ = DBSession_EA

    def get_applications(self):
        self.query = (self.__DBSession__.query(self.__model__).
                      options(subqueryload('properties').load_only("property", "value")).
                      options(load_only("name", "alias", "stereotype", "status", "note",
                                        "ea_guid", "gentype")).
                      outerjoin(TObject.properties, aliased=True).
                      outerjoin(TObject.packages, aliased=True).
                      filter(TObject.object_type == 'Package').
                      filter(TObject.stereotype.like('system%')).
                      filter(TPackage.parent_id.in_([74, 9054, 9055])))

        return self.run_query()

    @classmethod
    def get_app(cls, pk):
        return cls.get_by_pk(pk)

    @classmethod
    def edit_app(cls, obj, data):
        app = cls.update_model_object(obj, data)
        return cls.db_load(app)


class TagsAction(BaseAction):
    __model__ = TObjectproperty
    __DBSession__ = DBSession_EA

    @classmethod
    def get_tag(cls, pk):
        return cls.get_by_pk(pk)

    @classmethod
    def edit_tag(cls, obj, data):
        tag = cls.update_model_object(obj, data)
        return cls.db_load(tag)

    @classmethod
    def get_app_tags(cls, app_id):
        cls.query = (cls.__DBSession__.query(cls.__model__).
                     filter(cls.__model__.object_id == app_id))
        return cls.query.all()
