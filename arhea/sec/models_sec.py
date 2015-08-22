"""
Security models
"""
from sqlalchemy import (Column, Integer, String, ForeignKey, Index, Table)
from sqlalchemy.orm import (relationship)

from ..models import Base


#Security models
class User(Base):
    __tablename__ = 'sec_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    pwd = Column(String(100), nullable=False)
    #Many-to-many
    groups = relationship('Group', secondary='sec_user_groups', backref='sec_user')
    def __repr__(self):
        return '<User %r>' % (self.username)
    def __str__(self):
        return self.username

Index('sec_user_idx', User.username, unique=True)


class Group(Base):
    __tablename__ = 'sec_group'
    id = Column(Integer, primary_key=True)
    groupname = Column(String(60))
    users = relationship('User', secondary='sec_user_groups')
    def __repr__(self):
        return '<Group %r>' % (self.groupname)
    def __str__(self):
        return self.groupname


user_groups = Table('sec_user_groups', Base.metadata,
                    Column('user', Integer, ForeignKey('sec_user.id'), primary_key=True),
                    Column('group', Integer, ForeignKey('sec_group.id'), primary_key=True))
