"""
Application session handlers for every app_*
General models and application scope constants
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy import event, Column, String
from sqlalchemy.orm.attributes import get_history, History
from sqlalchemy.inspection import inspect

from zope.sqlalchemy import ZopeTransactionExtension
from pyramid.threadlocal import get_current_request

import logging
log = logging.getLogger(__name__)

#Session handler for local DB
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()),
                           scopefunc=get_current_request)
Base = declarative_base()

#Session handler for Enterprise Architect DB
DBSession_EA = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base_EA = declarative_base()


class LogMixin(object):
    """SqlAlchemy event listeners for logging. Declare model class Mixin extension"""

    def after_insert(mapper, connection, target):
        #do some stuff for the insert
        pass

    def after_update(mapper, connection, target):
        for field in mapper.columns.keys():
            hist = get_history(target, field)
            #import pdb; pdb.set_trace()
            if hist.has_changes():
                log.info('Application Update: {0}, PK: {1}, OLD: {2}, NEW: {3}, USER: {4}'.
                         format(mapper.class_, inspect(target).identity, hist.deleted,
                                hist.added, DBSession.registry.scopefunc().authenticated_userid))

    def after_delete(mapper, connection, target):
        #do some stuff
        pass

    @classmethod
    def __declare_last__(cls):
        event.listen(LogMixin, "after_insert", cls.after_insert, propagate=True)
        event.listen(LogMixin, "after_update", cls.after_update, propagate=True)
        event.listen(LogMixin, "after_delete", cls.after_delete, propagate=True)


#Pagination page row count
ITEMS_PER_PAGE = 5


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