"""
Apps package models
"""

from sqlalchemy import (Column, Integer, String, ForeignKey, Index, Table, text, Text, DateTime)
from sqlalchemy.orm import (relationship)

from ..models import Base_EA


class TObjectproperty(Base_EA):
    __tablename__ = 't_objectproperties'

    propertyid = Column(Integer, primary_key=True,
                        server_default=text("nextval(('propertyid_seq'::text)::regclass)"))
    object_id = Column(Integer, ForeignKey('t_object.object_id'),
                       index=True, server_default=text("0"))
    property = Column(String(255))
    value = Column(String(255))
    notes = Column(Text)
    ea_guid = Column(String(40))


class TObject(Base_EA):
    __tablename__ = 't_object'

    object_id = Column(Integer, primary_key=True, unique=True,
                       server_default=text("nextval(('object_id_seq'::text)::regclass)"))
    object_type = Column(String(255), index=True)
    diagram_id = Column(Integer, server_default=text("0"))
    name = Column(String(255))
    alias = Column(String(255))
    author = Column(String(255))
    version = Column(String(50), server_default=text("'1.0'::character varying"))
    note = Column(Text)
    package_id = Column(Integer, ForeignKey('t_package.package_id'),
                        index=True, server_default=text("0"))
    stereotype = Column(String(255))
    ntype = Column(Integer, index=True, server_default=text("0"))
    complexity = Column(String(50), server_default=text("'2'::character varying"))
    effort = Column(Integer, server_default=text("0"))
    createddate = Column(DateTime, server_default=text("now()"))
    modifieddate = Column(DateTime, server_default=text("now()"))
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

    packages = relationship("TPackage", backref="t_object", foreign_keys=[package_id])
    properties = relationship('TObjectproperty', primaryjoin=object_id == TObjectproperty.object_id)
    def __repr__(self):
        return '<EA_Object %r>' % (self.name)
    def __str__(self):
        return self.name

class TPackage(Base_EA):
    __tablename__ = 't_package'

    package_id = Column(Integer, primary_key=True, unique=True,
                        server_default=text("nextval(('package_id_seq'::text)::regclass)"))
    name = Column(String(255), index=True)
    parent_id = Column(Integer, index=True, server_default=text("0"))
    createddate = Column(DateTime, server_default=text("now()"))
    modifieddate = Column(DateTime, server_default=text("now()"))
    notes = Column(Text)
    ea_guid = Column(String(40), unique=True)
    xmlpath = Column(String(255))
    iscontrolled = Column(Integer, server_default=text("0"))
    lastloaddate = Column(DateTime)
    lastsavedate = Column(DateTime)
    version = Column(String(50))
    protected = Column(Integer, server_default=text("0"))
    pkgowner = Column(String(255))
    umlversion = Column(String(50))
    usedtd = Column(Integer, server_default=text("0"))
    logxml = Column(Integer, server_default=text("0"))
    codepath = Column(String(255))
    namespace = Column(String(50))
    tpos = Column(Integer)
    packageflags = Column(String(255))
    batchsave = Column(Integer)
    batchload = Column(Integer)

