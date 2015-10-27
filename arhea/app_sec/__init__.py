"""
Security package providing:
    - pyramid ACL configuration groups/permissions
    - userfinder and groupfinder functions
    - user and group management database backend with admin UI
__author__ = 'margusp'
"""
from ldap3 import Server, Connection, ALL
#LDAP config
ldap_server = 'ldap.elion.ee'
ldap_connection_account = 'CN=Margus Pärnsalu,OU=Telekom,OU=Inimesed,OU=ET,DC=et,DC=ee'
ldap_connection_pwd = 'Delly999'
ldap_user_base = 'OU=Inimesed,OU=ET,DC=et,DC=ee'
ldap_group_base = 'OU=Arhea,OU=Roll,OU=RBAC,OU=ET,DC=et,DC=ee'


conn = Connection(server='ldap.elion.ee', auto_bind=True)

def include(config):

    conn.user = ldap_connection_account
    conn.password = ldap_connection_pwd
    conn.use_ssl = True
    conn.get_info = ALL


    #Sec module template location
    config.add_jinja2_search_path('arhea:app_sec/templates')

    #Security login/logout
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    #Security_user
    config.add_route('user_view', '/sec/users')
    config.add_route('user_view:page', '/sec/users/page/{page:\d+}')
    config.add_route('user_add', '/sec/users/add')
    config.add_route('user_edit', '/sec/users/{usr_id:\d+}/edit')

    #Security_group
    config.add_route('group_view', '/sec/groups')
    config.add_route('group_view:page', '/sec/groups/page/{page:\d+}')
    config.add_route('group_add', '/sec/groups/add')
    config.add_route('group_edit', '/sec/groups/{gro_id:\d+}/edit')

