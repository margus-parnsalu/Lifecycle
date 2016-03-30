"""
App_apps actions module. Extends BaseAction from core.
"""
from sqlalchemy.orm import subqueryload, load_only
from sqlalchemy import func
from sqlalchemy.sql import label

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

    def get_domain_stats(self):
        self.query = (self.__DBSession__.query(TObject.status, TObjectproperty.value,
                                               label('count', func.count(TObject.name))).
                      outerjoin(TObjectproperty, TObject.object_id == TObjectproperty.object_id).
                      outerjoin(TPackage, TObject.package_id == TPackage.package_id).
                      filter(TObject.object_type == 'Package').
                      filter(TObject.stereotype.like('system%')).
                      filter(TPackage.parent_id.in_([74, 9054, 9055])).
                      filter(TObjectproperty.property == 'Development Domain').
                      filter(TObject.status != 'Proposed').
                      filter(TObject.status != 'Retired').
                      group_by(TObject.status, TObjectproperty.value).
                      order_by(TObjectproperty.value, TObject.status)
                      )

        return self.run_query()

    def get_lang_count(self):
        self.query = (self.__DBSession__.query(TObject.gentype,
                                               label('count', func.count(TObject.name))).
                      outerjoin(TPackage, TObject.package_id == TPackage.package_id).
                      filter(TObject.object_type == 'Package').
                      filter(TObject.stereotype.like('system%')).
                      filter(TPackage.parent_id.in_([74, 9054, 9055])).
                      group_by(TObject.gentype)
                      )

        return self.run_query()

    def get_app_count(self):
        self.query = (self.__DBSession__.query(label('count', func.count(TObject.name))).
                      outerjoin(TPackage, TObject.package_id == TPackage.package_id).
                      filter(TObject.object_type == 'Package').
                      filter(TObject.stereotype.like('system%')).
                      filter(TObject.status != 'Proposed').
                      filter(TObject.status != 'Retired').
                      filter(TPackage.parent_id.in_([74, 9054, 9055]))
                      )
        return self.run_query()[0]


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
