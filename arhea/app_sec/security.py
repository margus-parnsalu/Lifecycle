"""
Security core logic. Supports DB and LDAP.
"""
import hashlib
import logging
import datetime

from pyramid.security import Allow, Everyone
from pyramid.response import Response

from sqlalchemy.exc import DBAPIError
from sqlalchemy.sql import or_

# LDAP server connection from app_sec.__init__. To be used in queries
from . import conn

from .models_sec import (User, Group)
from ..models import (DBSession, conn_err_msg)

log = logging.getLogger(__name__)


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
        if userid == 'admin':  # admin is special user based on local groups
            groups = db_groups(userid)
        else:
            groups = ldap_groups(userid, request)
        session[session_groups] = groups
        log.info('USER "%s" LOGGED IN!', userid)
        return groups


def ldap_groups(userid, request):
    """Supporting function for groupfinder(). Groups based on ldap query"""
    groups = []
    settings = request.registry.settings
    ldap_user_base = settings['ldap.user_base']  # from ini config
    ldap_group_base = settings['ldap.group_base']  # from ini config

    user = userid.split('@')  # Admin Gateway returns user with domain @ET
    if conn.search(ldap_user_base, '(sAMAccountName={0})'.format(user[0])):
        user_dn = conn.entries[0].entry_get_dn()
        if conn.search(ldap_group_base, '(member={0})'.format(user_dn), attributes=['cn']):
            for raw_role in conn.entries:
                groups.append(raw_role.cn.value)   # value of the role in list

    return groups


def db_groups(userid):
    """Supporting function for groupfinder(). Groups based on DB query"""
    try:
        user_groups = (DBSession.query(Group.groupname).
                       filter(Group.users.any(username=userid)).
                       all())
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    groups = [r for (r, ) in user_groups]
    return groups


class RootFactory(object):
    """Pyramid ACL mapping of groups and view permissions"""
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'Viewers', 'view'),
               (Allow, 'Editors', ('edit_tag', 'edit_app')),
               (Allow, 'Arhea_Editors', ('edit_tag', 'edit_app')),
               (Allow, 'Arhea_Admins', ('admin')),
               (Allow, 'Admins', ('admin'))]

    def __init__(self, request):
        pass
