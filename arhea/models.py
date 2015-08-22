from sqlalchemy import (Column, Integer, String, Date, ForeignKey,
                        DateTime, Text, text, Index, Table)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (relationship, scoped_session, sessionmaker)

from zope.sqlalchemy import ZopeTransactionExtension


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

DBSession_EA = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base_EA = declarative_base()

class Employee(Base):
    __tablename__ = 'hr_employees'
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(25), nullable=False)
    email = Column(String(40))
    phone_number = Column(String(20))
    hire_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    salary = Column(Integer)

    department_id = Column(Integer, ForeignKey('hr_departments.department_id'))
    department = relationship("Department", backref="hr_employees", foreign_keys=[department_id])

    def __repr__(self):
        return '<Employee %r>' % (self.last_name)
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    def name(self):
        return self.first_name + ' ' + self.last_name



class Department(Base):
    __tablename__ = 'hr_departments'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(60), nullable=False)
    employees = relationship('Employee', primaryjoin=department_id==Employee.department_id)

    def __repr__(self):
        return '<Department %r>' % (self.department_name)
    def __str__(self):
        return self.department_name


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
    properties = relationship('TObjectproperty', primaryjoin=object_id==TObjectproperty.object_id)
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



def ea_applications():
    raw_q = """\
    select ea_guid as "GUID", stereotype as "Company", name as "Application",
    alias as "Alias", status as "Lifecycle", note as "Description"
    from t_object
    where stereotype='system' and object_type='Package'
    """
    return DBSession_EA.execute(raw_q).fetchall()




#Pagination page row count
ITEMS_PER_PAGE = 3

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_arhea_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""