"""
Security package providing:
    - pyramid ACL configuration groups/permissions
    - userfinder and groupfinder functions
    - user and group management database backend with UI
__author__ = 'margusp'
"""

def include(config):

    #Sec module template location
    config.add_jinja2_search_path('arhea:sec/templates')

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
