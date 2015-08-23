"""
Security module for login/logout and user/group management
"""
from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from ..models import (DBSession, conn_err_msg)
from .security import (userfinder)
from .forms_sec import (LoginForm, GroupForm, UserForm)
from .models_sec import (User, Group)


@view_config(route_name='login', renderer='login.jinja2',
             request_method=['GET', 'POST'], permission='view')
@forbidden_view_config(renderer='login.jinja2')#For customizing default 404 forbidden template
def login(request):
    """User login form"""
    came_from = request.referer or request.route_url('home')
    login_url = request.route_url('login')
    if came_from == login_url:
        came_from = '/' # never use the login form itself as came_from
    login_val = ''
    form = LoginForm(request.POST, came_from, login_val, csrf_context=request.session)
    message = ''
    if request.method == 'POST' and form.validate():
        login_user = request.params['login']
        password = request.params['password']
        if userfinder(login_user, password):
            headers = remember(request, login_user)
            request.session.flash('User: '+ login_user + ' logged in!')
            return HTTPFound(location=came_from, headers=headers)
        request.session.flash('Failed login!', queue='fail', allow_duplicate=False)

    return {'form' : form,
            'message' : message,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='logout',
             permission='view')
def logout(request):
    """Logout, forget user"""
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)



@view_config(route_name='user_view', renderer='user_r.jinja2',
             request_method=['GET', 'POST'], permission='admin')
def user_view(request):
    try:
        users = DBSession.query(User).order_by(text('upper(sec_user.username) asc')).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'users': users,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='user_add', renderer='user_f.jinja2',
             request_method=['GET', 'POST'], permission='admin')
def user_add(request):
    form = UserForm(request.POST, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        usr = User(username=form.username.data,
                   pwd=form.pwd.data,
                   groups=form.groups.data)
        DBSession.add(usr)
        request.session.flash('User Added!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('user_view'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='user_edit', renderer='user_f.jinja2',
             request_method=['GET', 'POST'], permission='admin')
def user_edit(request):
    try:
        user = DBSession.query(User).get(request.matchdict['usr_id'])
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    form = UserForm(request.POST, user, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        user.username = form.username.data
        user.pwd = form.pwd.data
        user.groups = form.groups.data
        DBSession.add(user)
        request.session.flash('User Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('user_view'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='group_view', renderer='group_r.jinja2',
             request_method=['GET', 'POST'], permission='admin')
@view_config(route_name='group_view:page', renderer='group_r.jinja2',
             request_method=['GET', 'POST'], permission='admin')
def group_view(request):

    try:
        groups = DBSession.query(Group).order_by(text('upper(sec_group.groupname) asc')).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'groups': groups,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='group_add', renderer='group_f.jinja2',
             request_method=['GET', 'POST'], permission='admin')
def group_add(request):
    form = GroupForm(request.POST, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        gro = Group(groupname=form.groupname.data)
        DBSession.add(gro)
        request.session.flash('Group Added!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('group_view'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='group_edit', renderer='group_f.jinja2',
             request_method=['GET', 'POST'], permission='admin')
def group_edit(request):
    try:
        group = DBSession.query(Group).get(request.matchdict['gro_id'])
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    form = GroupForm(request.POST, group, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        group.groupname = form.groupname.data
        DBSession.add(group)
        request.session.flash('Group Updated!', allow_duplicate=False)
        return HTTPFound(location=request.route_url('group_view'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}
