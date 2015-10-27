"""
Security package providing:
    - pyramid ACL configuration groups/permissions
    - userfinder and groupfinder functions
    - user and group management database backend with admin UI
__author__ = 'margusp'
"""
from ldap3 import Server, Connection, ALL
#LDAP config
server = Server('ldap.elion.ee', use_ssl=True, get_info=ALL)
conn = Connection(server=server, auto_bind=True)

def include(config):

    # Reconfigure ldap3 connection with account from config
    settings = config.registry.settings
    conn.user = settings['ldap.user']
    conn.password = settings['ldap.pwd']
    conn.authentication = 'SIMPLE'
    conn.bind()


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

