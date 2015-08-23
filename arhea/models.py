"""
Application session handlers for every app_*
General models and application scope constants
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)

from zope.sqlalchemy import ZopeTransactionExtension


#Session handler for local DB
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

#Session handler for Enterprise Architect DB
DBSession_EA = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base_EA = declarative_base()



#Pagination page row count
ITEMS_PER_PAGE = 3


#DBAPI error message
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