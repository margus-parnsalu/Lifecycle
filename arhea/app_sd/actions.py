"""
SD_apps actions module. Extends BaseAction from core.
"""
from sqlalchemy.orm import subqueryload, load_only
from sqlalchemy import func
from sqlalchemy.sql import label

from ..actions import BaseAction
from ..models import DBSession

from .models import CI
import requests
import json
import logging
import datetime

log = logging.getLogger(__name__)


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
        cls.__DBSession__.query(cls.__model__).delete()
        cls.__DBSession__.flush()

    def get_internal_cis(self):
        self.query = (self.__DBSession__.query(self.__model__).
                     filter(self.__model__.owner.in_(['ELION', 'TELIAEESTI', 'EMT'])).
                     filter(self.__model__.code.like('%-LIVE')))
        return  self.run_query()

    @staticmethod
    def replicate_ci(user, pwd, host):

        start = datetime.datetime.now()

        r = requests.get(host + '/sd_api_new/rest/ci/category/application', auth=(user, pwd))
        if r.status_code == 200:
            CIAction.purge()  # Clean db from CI-s.
            codes = json.loads(r.content.decode('UTF-8'))
            for code in codes:
                r = requests.get(host + '/sd_api_new/rest/ci/' + code['code'], auth=(user, pwd))
                if r.status_code == 200:
                    ci_data = json.loads(r.content.decode('UTF-8'))
                    data = {}
                    data['code'] = ci_data['code']
                    data['system_id'] = ci_data['system_id']
                    data['name'] = ci_data['name']
                    data['owner'] = ci_data['owner']
                    data['remark'] = ci_data['remark']
                    data['performer1'] = ci_data['performer1']
                    data['performer2'] = ci_data['performer2']
                    data['performer_new'] = ci_data['future_performer1']

                    if ci_data['owner'] in ['ELION', 'TELIAEESTI', 'EMT']:
                        CIAction.create_ci(data)

            end = datetime.datetime.now()
            log.info(('CI Replica - when: {0}; time: {1}').format(start, end-start ))
            return 'OK'
        return 'NOK'
