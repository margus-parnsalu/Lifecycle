"""
App_apps actions module. Extends BaseAction from core.
"""
from sqlalchemy.orm import subqueryload, load_only

from ..core import BaseAction
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

    def get_app(self, pk):
        return self.get_by_pk(pk)



class TagsAction(BaseAction):
    __model__ = TObjectproperty
    __DBSession__ = DBSession_EA

    def get_tag(self, pk):
        return self.get_by_pk(pk)

    def edit_tag(self, model, form):
        tag = self.edit_form_model(model, form)
        return self.db_load(tag)

    def get_app_tags(self, app_id):
        self.query = (self.query.filter(self.__model__.object_id == app_id))
        return self.run_query()



