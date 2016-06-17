import os
import sys
import transaction
import hashlib

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Base,
    DBSession_EA,
    Base_EA
    )
from ..app_hr.models_hr import (Employee, Department)
from ..app_sec.models_sec import (User, Group, user_groups)
from ..app_sd.models import (CI)



def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.default.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    #Starter admin and viewer, editor account
    #with transaction.manager:
    #   grp1 = Group(groupname='Admins')
    #    grp2 = Group(groupname='Editors')
    #    grp3 = Group(groupname='Viewers')
    #    usr1 = User(username='admin',
    #                pwd=hashlib.sha256((settings['starter.admin']).encode()).hexdigest(),
    #                groups=[grp1, grp2])
    #    usr2 = User(username='editor',
    #                pwd=hashlib.sha256(('editor').encode()).hexdigest(),
    #                groups=[grp2])
    #    usr3 = User(username='viewer',
    #                pwd=hashlib.sha256(('viewer').encode()).hexdigest(),
    #                groups=[grp3])
    #    DBSession.add(grp1)
    #    DBSession.add(grp2)
    #    DBSession.add(grp3)
    #    DBSession.add(usr1)
    #    DBSession.add(usr2)
    #    DBSession.add(usr3)


    #engine2 = engine_from_config(settings, 'sqlalchemy.ea.')
    #DBSession_EA.configure(bind=engine2)
    #Base_EA.metadata.create_all(engine2)

