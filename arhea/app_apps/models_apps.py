"""
Apps package models
"""

from sqlalchemy import (Column, Integer, String, ForeignKey, Index, Table, text, Text, DateTime)
from sqlalchemy.orm import (relationship)

from ..models import Base_EA, LogMixin, DBSession_EA


class TObjectproperty(Base_EA, LogMixin):
    __tablename__ = 't_objectproperties'

    propertyid = Column(Integer, primary_key=True)
    object_id = Column(Integer, ForeignKey('t_object.object_id'),
                       index=True)
    property = Column(String(255))
    value = Column(String(255))
    notes = Column(Text)
    ea_guid = Column(String(40))
    def __repr__(self):
        return '<EA_Objectproperty %r>' % (self.property)
    def __str__(self):
        return self.property


class TObject(Base_EA, LogMixin):
    __tablename__ = 't_object'

    object_id = Column(Integer, primary_key=True, unique=True)
    object_type = Column(String(255), index=True)
    diagram_id = Column(Integer)
    name = Column(String(255))
    alias = Column(String(255))
    author = Column(String(255))
    version = Column(String(50))
    note = Column(Text)
    package_id = Column(Integer, ForeignKey('t_package.package_id'),
                        index=True)
    stereotype = Column(String(255))
    ntype = Column(Integer, index=True)
    complexity = Column(String(50))
    effort = Column(Integer)
    createddate = Column(DateTime)
    modifieddate = Column(DateTime)
    status = Column(String(50))
    abstract = Column(String(1))
    classifier = Column(Integer, index=True)
    ea_guid = Column(String(40), unique=True)
    parentid = Column(Integer, index=True)
    runstate = Column(Text)
    classifier_guid = Column(String(40), index=True)
    tpos = Column(Integer)
    stateflags = Column(String(255))
    packageflags = Column(String(255))
    multiplicity = Column(String(50))
    styleex = Column(Text)
    gentype = Column(String(50))

    packages = relationship("TPackage", backref="t_object", foreign_keys=[package_id])
    properties = relationship('TObjectproperty', primaryjoin=object_id == TObjectproperty.object_id,
                              order_by="TObjectproperty.property")
    def __repr__(self):
        return '<EA_Object %r>' % (self.name)
    def __str__(self):
        return self.name


class TPackage(Base_EA):
    __tablename__ = 't_package'

    package_id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), index=True)
    parent_id = Column(Integer, index=True)
    createddate = Column(DateTime)
    modifieddate = Column(DateTime)
    notes = Column(Text)
    ea_guid = Column(String(40), unique=True)
    xmlpath = Column(String(255))
    iscontrolled = Column(Integer)
    lastloaddate = Column(DateTime)
    lastsavedate = Column(DateTime)
    version = Column(String(50))
    protected = Column(Integer)
    pkgowner = Column(String(255))
    umlversion = Column(String(50))
    usedtd = Column(Integer)
    logxml = Column(Integer)
    codepath = Column(String(255))
    namespace = Column(String(50))
    tpos = Column(Integer)
    packageflags = Column(String(255))
    batchsave = Column(Integer)
    batchload = Column(Integer)


class TDatatype(Base_EA):
    __tablename__ = 't_datatypes'

    type = Column(String(50))
    productname = Column(String(50))
    datatype = Column(String(50))
    haslength = Column(String(50))
    generictype = Column(String(255))
    datatypeid = Column(Integer, primary_key=True)


def languages_lov():
    languages = (DBSession_EA.query(TDatatype.productname.distinct(), TDatatype.productname).
                 filter(TDatatype.type == 'Code').
                 order_by(TDatatype.productname.asc()))
    return [('<none>', '<none>')] + [(k, v) for (k, v) in languages]