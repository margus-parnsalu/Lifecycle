"""
App_apps actions module. Extends BaseAction from core.
"""
from sqlalchemy.orm import subqueryload, load_only

from ..core import BaseAction
from ..models import DBSession_EA

from.models_apps import TObject, TPackage


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
