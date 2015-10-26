"""
Security core logic
LDAP with pyramid_ldap
"""
import hashlib, logging, datetime

from pyramid.security import (Allow, Everyone)
from pyramid.response import Response

from ldap3 import Server, Connection, ALL

from sqlalchemy.exc import DBAPIError
from sqlalchemy import or_

from .models_sec import (User, Group)
from ..models import (DBSession, conn_err_msg)

log = logging.getLogger(__name__)

# Creating ldap server connection
server = Server('ldap.elion.ee', use_ssl=True, get_info=ALL)
conn = Connection(server, 'CN=Margus Pärnsalu,OU=Telekom,OU=Inimesed,OU=ET,DC=et,DC=ee',
                          'Delly999', auto_bind=True)


def userfinder(userid, password):
    """Validate user login in login view"""
    found = False
    try:
        usermatch = (DBSession.query(User).
                     filter(User.username == userid).
                     filter(or_(User.end_date == None, User.end_date > datetime.datetime.now())).
                     first())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    if usermatch and hashlib.sha256(password.encode()).hexdigest() == usermatch.pwd:
        found = True
    return found


def groupfinder(userid, request):
    """Find groups where user belongs to"""
    session = request.session
    session_groups = 'user_groups'

    if session_groups in session:
        return session[session_groups]
    elif userid:
        groups = ldap_groups(userid)
        session[session_groups] = groups
        log.info('USER "%s" LOGGED IN!', userid)
        return groups


def ldap_groups(userid):
    """Supporting function for groupfinder(). Groups based on ldap query"""
    groups = []
    ldap_user_base = 'OU=Inimesed,OU=ET,DC=et,DC=ee'
    ldap_group_base = 'OU=Arhea,OU=Roll,OU=RBAC,OU=ET,DC=et,DC=ee'
    user = userid.split('@')  # Admin Gateway returns user with domain @ET
    if conn.search(ldap_user_base, '(sAMAccountName={0})'.format(user[0])):
        user_dn = conn.entries[0].entry_get_dn()
        if conn.search(ldap_group_base, '(member={0})'.format(user_dn), attributes=['cn']):
            for raw_role in conn.entries:
                groups.append(raw_role.cn.value)   # value of the role in list
    return groups


class RootFactory(object):
    """Pyramid ACL mapping of groups and view permissions"""
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'Viewers', 'view'),
               (Allow, 'Arhea_Editors', 'edit'),
               (Allow, 'Admins', ('admin', 'edit'))]

    def __init__(self, request):
        pass
