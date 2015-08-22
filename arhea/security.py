from pyramid.security import (Allow, Everyone)

from .models import DBSession, User, Group

USERS = {'editor':'editor',
         'viewer':'viewer'}
GROUPS = {'editor':['group:editors'],
          'margusp@ET.EE':['group:editors']}


# Validate user login in view
def userfinder(userid, password):
    found = False
    usermatch = DBSession.query(User).filter(User.username==userid).first()
    if usermatch and usermatch.pwd==password:
        found = True
    return found

def groupfinder(userid, request):
    if userid:
        user_groups = DBSession.query(Group.groupname).filter(Group.users.any(username=userid)).all()
        groups = [r for (r, ) in user_groups]
        return groups



class RootFactory(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'Viewers', 'view'),
               (Allow, 'Editors', 'edit'),
               (Allow, 'Admins', 'admin')]
    def __init__(self, request):
        pass





