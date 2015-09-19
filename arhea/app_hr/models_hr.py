"""
HR Models
"""
from sqlalchemy import (Column, Integer, String, Date, ForeignKey,
                        DateTime, Text, text, Index, Table)
from sqlalchemy.orm import (relationship)

from ..models import Base, LogMixin



class Employee(Base, LogMixin):
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


class Department(Base, LogMixin):
    __tablename__ = 'hr_departments'
    department_id = Column(Integer, primary_key=True)
    department_name = Column(String(60), nullable=False)
    employees = relationship('Employee', primaryjoin=department_id==Employee.department_id)

    def __repr__(self):
        return '<Department %r>' % (self.department_name)
    def __str__(self):
        return self.department_name

