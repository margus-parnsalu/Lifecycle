"""
Security forms
"""
from wtforms import (validators, StringField, HiddenField, PasswordField, DateTimeField)
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import PasswordInput

from ..forms import BaseForm
from ..models import DBSession
from .models_sec import Group


def groups():
    """Group LOV"""
    return DBSession.query(Group).all()


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
    groups = QuerySelectMultipleField(u'Groups', query_factory=groups, allow_blank=True)
    end_date = DateTimeField(u'End Date', [validators.Optional()], format='%Y-%m-%d %H:%M')
