from pyramid.view import view_config, forbidden_view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.response import Response
from pyramid.security import remember, forget, authenticated_userid

from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from paginate import Page

from ..security import (userfinder)
from ..forms import (LoginForm, GroupForm, UserForm)
from ..models import (DBSession, User, Group, conn_err_msg, ITEMS_PER_PAGE)

@view_config(route_name='login', renderer='login.jinja2', request_method=['GET','POST'], permission='view')
@forbidden_view_config(renderer='login.jinja2')#For customizing default 404 forbidden template
def login(request):
    came_from = request.referer or request.route_url('home')
    login_url = request.route_url('login')
    if came_from == login_url:
        came_from = '/' # never use the login form itself as came_from
    login = ''
    form = LoginForm(request.POST, came_from, login, csrf_context=request.session)
    message = ''

    #import pdb; pdb.set_trace()

    if request.method == 'POST' and form.validate():
        login_user = request.params['login']
        password = request.params['password']

        if userfinder(login_user, password):
            headers = remember(request, login_user)
            request.session.flash('User: '+ login_user + ' logged in!')
            return HTTPFound(location=came_from, headers=headers)
        message = 'Failed login!'
    return {'form' : form,
            'message' : message,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='logout',
             permission='view')
def logout(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)



@view_config(route_name='user_view', renderer='user_r.jinja2', request_method=['GET','POST'],
             permission='admin')
def user_view(request):
    try:
        users = DBSession.query(User).order_by(text('upper(sec_user.username) asc')).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'users': users,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='user_add', renderer='user_f.jinja2', request_method=['GET','POST'],
             permission='admin')
def user_add(request):
    form = UserForm(request.POST, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        usr = User()
        form.populate_obj(usr)
        #Employee(username=form.username.data, pwd=form.pwd.data)
        DBSession.add(usr)
        request.session.flash('User Added!')
        return HTTPFound(location=request.route_url('home'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='user_edit', renderer='user_f.jinja2', request_method=['GET','POST'],
             permission='admin')
def user_edit(request):
    try:
        user = DBSession.query(User).get(request.matchdict['usr_id'])
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    form = UserForm(request.POST, user, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        form.populate_obj(user)
        DBSession.add(user)
        request.session.flash('User Updated!')
        return HTTPFound(location=request.route_url('home'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='group_view', renderer='group_r.jinja2',
             request_method=['GET','POST'], permission='admin')
@view_config(route_name='group_view:page', renderer='group_r.jinja2',
             request_method=['GET','POST'], permission='admin')
def group_view(request):

    try:
        groups = DBSession.query(Group).order_by(text('upper(sec_group.groupname) asc')).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)

    return {'groups': groups,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='group_add', renderer='group_f.jinja2', request_method=['GET','POST'],
             permission='admin')
def group_add(request):
    form = GroupForm(request.POST, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        gro = Group(groupname=form.groupname.data)
        DBSession.add(gro)
        request.session.flash('Group Added!')
        return HTTPFound(location=request.route_url('group_view'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}


@view_config(route_name='group_edit', renderer='group_f.jinja2', request_method=['GET','POST'],
             permission='admin')
def group_edit(request):
    try:
        group = DBSession.query(Group).get(request.matchdict['gro_id'])
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    form = GroupForm(request.POST, group, csrf_context=request.session)
    if request.method == 'POST' and form.validate():
        form.populate_obj(group)
        DBSession.add(group)
        request.session.flash('Group Updated!')
        return HTTPFound(location=request.route_url('group_view'))
    return {'form': form,
            'logged_in': authenticated_userid(request)}
