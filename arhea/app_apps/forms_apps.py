"""
Apps package forms
"""
from wtforms import (validators, StringField, HiddenField, SelectField, Form,
                     TextAreaField, FormField, FieldList, IntegerField)
from wtforms.widgets import HiddenInput
from ..forms import BaseForm


class ApplicationForm(Form):
    object_id = IntegerField(widget=HiddenInput())
    stereotype = (SelectField(u'Brand', choices=[("", 'Brand'),
                                                 ("", '------'),
                                                 ('system', 'Telekom'),
                                                 ('system Elion', 'Elion'),
                                                 ('system EMT', 'EMT')]))
    name = StringField(u'Name', [validators.Length(min=2, max=50)])
    alias = StringField(u'Alias', [validators.Optional(), validators.Length(min=2, max=50)])
    note = TextAreaField(u'Note', [validators.Length(min=0, max=500)])
    gentype = SelectField(u'Language')
    status = (SelectField(u'Lifecycle', choices=[("", 'Lifecycle'),
                                                 ("", '------'),
                                                 ('Target', 'Target'),
                                                 ('Acceptable', 'Acceptable'),
                                                 ('Freeze', 'Freeze'),
                                                 ('Phase Out', 'Phase Out'),
                                                 ('Proposed', 'Proposed'),
                                                 ('Retired', 'Retired')]))


class InlineTagForm(Form):
    """Unsecure Form for multiline edit Tag Values"""
    propertyid = IntegerField(widget=HiddenInput())
    object_id = IntegerField(widget=HiddenInput())
    property = StringField(u'Tag Name', [validators.Length(min=3, max=250)])
    value = StringField(u'Tag Value', [validators.Length(min=1, max=250)])
    notes = HiddenField()
    ea_guid = HiddenField()
    domain_list = (SelectField(u'Domain list', [validators.Optional()],
                   choices=[("", 'Vali väärtus listist!'),
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


class TagUpdateForm(BaseForm, InlineTagForm):
    """Secure form for updating Tag Values"""
    pass

class ApplicationTagForm(BaseForm):
    """Master-Detail form for updating application and related tag information"""
    app = FormField(ApplicationForm)
    tags = FieldList(FormField(InlineTagForm), max_entries=6)
