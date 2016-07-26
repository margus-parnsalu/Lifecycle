import transaction
from datetime import timedelta

from celeryconfig import app

from arhea.app_sd.actions import CIAction


# Celery beat config
app.conf.update(
    CELERYBEAT_SCHEDULE = {
        'replicate_ci':
            {
                'task': 'tasks.replicate_ci',
                'schedule': timedelta(minutes=20)
            },
    }
)


@app.task
def replicate_ci():
    host = app.settings['sd.host']
    user = app.settings['sd.user']
    pwd = app.settings['sd.pwd']

    CIAction.replicate_ci(user, pwd, host)
    transaction.commit()
