"""
Apps package forms
"""
from wtforms import (validators, StringField, HiddenField, PasswordField, SelectField, Form)
from ..forms import BaseForm

class ApplicationForm(Form):
    stereotype = (SelectField(u'Brand', choices=[("", 'Brand'),
                                                 ("", '------'),
                                                 ('system', 'Telekom'),
                                                 ('system Elion', 'Elion'),
                                                 ('system EMT', 'EMT')]))
    name = StringField(u'Name', [validators.Length(min=3, max=50)])
    alias = StringField(u'Alias', [validators.Length(min=3, max=50)])
    status = (SelectField(u'Lifecycle', choices=[("", 'Lifecycle'),
                                                 ("", '------'),
                                                 ('Target', 'Target'),
                                                 ('Acceptable', 'Acceptable'),
                                                 ('Freeze', 'Freeze'),
                                                 ('Phase Out', 'Phase Out')]))

class TagUpdateForm(BaseForm):
    """Form for updating Tag Values"""
    propertyid = HiddenField()
    object_id = HiddenField()
    property = StringField(u'Tag Name', [validators.Length(min=3, max=250)])
    value = StringField(u'Tag Value', [validators.Length(min=3, max=250)])
    notes = HiddenField()
    ea_guid = HiddenField()
    domain_list = (SelectField(u'Domain list', choices=[("", 'Vali väärtus listist!'),
                                                        ("", '------'),
                                                        ('Kliendihaldus', 'Kliendihaldus'),
                                                        ('Müük ja Tarne', 'Müük ja Tarne'),
                                                        ('Arveldus ja võlgnevuste haldus', 'Arveldus ja võlgnevuste haldus'),
                                                        ('IT infra/haldusvahendid', 'IT infra/haldusvahendid'),
                                                        ('Kasutajatugi', 'Kasutajatugi'),
                                                        ('Ettevõtte tugi ja kaubamüük', 'Ettevõtte tugi ja kaubamüük'),
                                                        ('Riski- ja turbejuhtimine', 'Riski- ja turbejuhtimine'),
                                                        ('Andmeait', 'Andmeait'),
                                                        ('Ressursiregistrid', 'Ressursiregistrid'),
                                                        ('Põhiteenused ja pakkumised', 'Põhiteenused ja pakkumised'),
                                                        ('TV ja meedia', 'TV ja meedia'),
                                                        ('IT teenused', 'IT teenused'),
                                                        ('Suhtlus ja Portaalid', 'Suhtlus ja Portaalid'),
                                                        ('Lisateenused ja uurimistöö', 'Lisateenused ja uurimistöö')]))
