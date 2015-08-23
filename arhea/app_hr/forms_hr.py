"""
HR Forms
"""
from wtforms import (validators, StringField, IntegerField, DateField)
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from ..forms import BaseForm
from ..models import DBSession
from .models_hr import Department


#LOV ehk Query_factory Departments jaoks
def Departments():
    return DBSession.query(Department).all()



class DepartmentForm(BaseForm):
    department_name = (StringField(u'Department Name',
                                   [validators.Length(min=3, max=60),
                                    validators.InputRequired(message=(u'Input Department Name'))]))


class EmployeeForm(BaseForm):
    first_name = (StringField(u'First Name',
                              [validators.Length(min=4, max=64),
                               validators.InputRequired(message=(u'Input First Name'))]))
    last_name = (StringField(u'Last Name',
                             [validators.Length(min=4, max=64),
                              validators.InputRequired(message=(u'Input Last Name'))]))
    email = (StringField(u'E-mail', [validators.Email(),
                                     validators.InputRequired(message=(u'Input E-mail'))]))
    phone_number = (StringField(u'Phone Number',
                                [validators.Length(min=4, max=20),
                                 validators.InputRequired(message=(u'Input Phone Number'))]))
    salary = IntegerField(u'Salary', [validators.InputRequired(message=(u'Input Salary'))])
    hire_date = (DateField(u'Hire Date',
                           [validators.InputRequired(message=(u'Select Hire Date'))],
                           format='%d-%m-%Y'))
    end_date = DateField(u'End Date', [validators.Optional()], format='%d-%m-%Y')
    department = (QuerySelectField('Department',
                                   [validators.DataRequired()],
                                   query_factory=Departments, allow_blank=True))

