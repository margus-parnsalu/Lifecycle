from celery import Celery
from celery.signals import worker_init

from sqlalchemy import engine_from_config
from arhea.models import (DBSession, Base)


# When worker starts this gets the config from .ini file
@worker_init.connect
def bootstrap_pyramid(signal, sender):
    from pyramid.paster import bootstrap
    sender.app.settings = bootstrap('../dev.ini')['registry'].settings

    #SqlAlchemy:
    engine = engine_from_config(sender.app.settings, 'sqlalchemy.default.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

app = Celery('tasks', broker='redis://localhost:6379/0')

