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