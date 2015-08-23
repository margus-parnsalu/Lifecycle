"""
Apps package forms
"""
from wtforms import (validators, StringField, HiddenField, PasswordField, SelectField, Form)


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
