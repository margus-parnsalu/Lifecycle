from pyramid.security import (Allow, Everyone)
from pyramid.response import Response
from sqlalchemy.exc import DBAPIError
from .models import DBSession, conn_err_msg, User, Group

# Validate user login in view
def userfinder(userid, password):
    found = False
    try:
        usermatch = DBSession.query(User).filter(User.username==userid).first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    if usermatch and usermatch.pwd==password:
        found = True
    return found

def groupfinder(userid, request):
    if userid:
        try:
            user_groups = DBSession.query(Group.groupname).filter(Group.users.any(username=userid)).all()
        except DBAPIError:
            return Response(conn_err_msg, content_type='text/plain', status_int=500)

        groups = [r for (r, ) in user_groups]
        return groups


class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'Viewers', 'view'),
               (Allow, 'Editors', 'edit'),
               (Allow, 'Admins', ('admin', 'edit'))]
    def __init__(self, request):
        pass





