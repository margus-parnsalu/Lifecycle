"""
HPSD analyses models
"""
from sqlalchemy import (Column, String)


from ..models import Base


class CI(Base):
    __tablename__ = 'sd_ci'
    code = Column(String(50), primary_key=True)
    system_id = Column(String(50))
    name = Column(String(50))
    owner = Column(String(20))
    remark = Column(String(100))
    performer1 = Column(String(30))
    performer2 = Column(String(30))
    performer_new = Column(String(30))

    def __repr__(self):
        return '<CI %r>' % (self.code)
    def __str__(self):
        return self.code