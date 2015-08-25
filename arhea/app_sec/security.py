"""
Security core logic
"""
from pyramid.security import (Allow, Everyone)
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError

import hashlib

from .models_sec import (User, Group)
from ..models import (DBSession, conn_err_msg)


def userfinder(userid, password):
    """Validate user login in login view"""
    found = False
    try:
        usermatch = DBSession.query(User).filter(User.username == userid).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    if usermatch and hashlib.sha256((password).encode()).hexdigest() == usermatch.pwd:
        found = True
    return found


def groupfinder(userid, request):
    """Find groups where user belongs to"""
    session = request.session
    session_groups = 'user_groups'

    if session_groups in session:
        return session[session_groups]
    elif userid:
        try:
            user_groups = (DBSession.query(Group.groupname).
                           filter(Group.users.any(username=userid)).
                           all())
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)

        groups = [r for (r, ) in user_groups]
        session[session_groups] = groups
        return groups


class RootFactory(object):
    """Pyramid ACL mapping of groups and view permissions"""
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'Viewers', 'view'),
               (Allow, 'Editors', 'edit'),
               (Allow, 'Admins', ('admin', 'edit'))]
    def __init__(self, request):
        pass





