from wtforms import (validators, StringField, IntegerField, DateField, HiddenField, PasswordField,
                     SelectField, Form)
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.ext.csrf.session import SessionSecureForm
from wtforms.validators import ValidationError
from wtforms.widgets import PasswordInput

from .models import DBSession, Department, Group

#LOV ehk Query_factory Departments jaoks
def Departments():
    return DBSession.query(Department).all()

def Groups():
    return DBSession.query(Group).all()

#For CSRF security override with Pyramid session get_csrf_token
class BaseForm(SessionSecureForm):
    def generate_csrf_token(self, session):
        """Get the session's CSRF token."""
        return session.get_csrf_token()

    def validate_csrf_token(form, field):
        """Validate the CSRF token."""
        if field.data != field.current_token:
            raise ValidationError('Invalid CSRF token; the form probably expired.  Try again.')


class LoginForm(BaseForm):
    came_from = HiddenField(u'Came_from')
    login = StringField(u'Login')
    password = PasswordField(u'Password')

#Security module forms
class GroupForm(BaseForm):
    groupname = StringField(u'Group Name', [validators.Length(min=3, max=30),
                                         validators.InputRequired(message=(u'Input required'))])

class UserForm(BaseForm):
    username = StringField(u'Username', [validators.Length(min=3, max=30),
                                         validators.InputRequired(message=(u'Input First Name'))])
    pwd = PasswordField(u'Password', [validators.InputRequired(message=(u'Password required'))],
                        widget=PasswordInput(hide_value=False))
    groups = QuerySelectMultipleField(u'Groups', query_factory=Groups, allow_blank=True)



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

class ApplicationForm(Form):
     stereotype = (SelectField(u'Brand', choices=[("", 'Brand'), ("", '------'),
                                                  ('system', 'Telekom'),
                                                  ('system Elion', 'Elion'),
                                                  ('system EMT', 'EMT')]))
     name = StringField(u'Name', [validators.Length(min=3, max=50)])
     alias = StringField(u'Alias', [validators.Length(min=3, max=50)])
     status = (SelectField(u'Lifecycle', choices=[("", 'Lifecycle'), ("", '------'),
                                                  ('Target', 'Target'),
                                                  ('Acceptable', 'Acceptable'),
                                                  ('Freeze', 'Freeze'),
                                                  ('Phase Out', 'Phase Out')]))
