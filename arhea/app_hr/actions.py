"""
App_hr actions module. Extends BaseAction from core.
"""
from ..core import BaseAction
from .models_hr import Department, Employee


class DepartmentAction(BaseAction):
    __model__ = Department


    def get_departments(self):
        return self.run_query()

    @classmethod
    def get_department(cls, pk):
        return cls.get_by_pk(pk)

    @classmethod
    def add_department(cls, data):
        dep = cls.create_model_object(data)
        return cls.db_load(dep)

    @classmethod
    def edit_department(cls, object, data):
        dep = cls.update_model_object(object, data)
        return cls.db_load(dep)


class EmployeeAction(BaseAction):
    __model__ = Employee

    def get_employees(self):
        self.query = (self.__DBSession__.query(self.__model__, Department).
                      outerjoin(Department,
                                self.__model__.department_id == Department.department_id))
        return self.run_query()

    @classmethod
    def get_employee(cls, pk):
        return cls.get_by_pk(pk)

    @classmethod
    def add_employee(cls, form):
        emp = cls.add_form_model(form)
        return cls.db_load(emp)

    @classmethod
    def edit_employee(cls, model, form):
        emp = cls.edit_form_model(model, form)
        return cls.db_load(emp)
