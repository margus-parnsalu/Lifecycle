"""
App_hr actions module. Extends BaseAction from core.
"""
from ..core import BaseAction
from .models_hr import Department, Employee


class DepartmentAction(BaseAction):
    __model__ = Department

    def get_departments(self):
        return self.run_query()

    def get_department(self, pk):
        return self.get_by_pk(pk)

    def add_department(self, form):
        dep = self.add_form_model(form)
        return self.db_load(dep)

    def edit_department(self, model, form):
        dep = self.edit_form_model(model, form)
        return self.db_load(dep)


class EmployeeAction(BaseAction):
    __model__ = Employee

    def get_employees(self):
        self.query = (self.__DBSession__.query(self.__model__, Department).
                      outerjoin(Department,
                                self.__model__.department_id == Department.department_id))
        return self.run_query()

    def get_employee(self, pk):
        return self.get_by_pk(pk)

    def add_employee(self, form):
        emp = self.add_form_model(form)
        return self.db_load(emp)

    def edit_employee(self, model, form):
        emp = self.edit_form_model(model, form)
        return self.db_load(emp)
