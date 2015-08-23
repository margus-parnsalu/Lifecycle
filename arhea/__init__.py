from pyramid.config import Configurator
#Session Cookie setup
from pyramid.session import SignedCookieSessionFactory
#Security
from pyramid.authentication import AuthTktAuthenticationPolicy, RemoteUserAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid_multiauth import MultiAuthenticationPolicy
#DB connection
from sqlalchemy import engine_from_config

from .app_sec.security import groupfinder, RootFactory
from .models import (DBSession, Base, DBSession_EA, Base_EA)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    #Session factory (CSRF)
    my_session_factory = SignedCookieSessionFactory(settings['session.secret'])

    #SqlAlchemy:
    engine = engine_from_config(settings, 'sqlalchemy.default.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    engine2 = engine_from_config(settings, 'sqlalchemy.ea.')
    DBSession_EA.configure(bind=engine2)
    Base_EA.metadata.bind = engine2

    #Security
    #authn_policy = RemoteUserAuthenticationPolicy(environ_key='REMOTE_USER', callback=groupfinder)
    #authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder, hashalg='sha512')
    authz_policy = ACLAuthorizationPolicy()

    #Pyramid_multiauth seperate module for REMOTE_USER fallback
    policies = [
        RemoteUserAuthenticationPolicy(environ_key='HTTP_PROXY_AD_USER', callback=groupfinder),
        AuthTktAuthenticationPolicy(settings['auth.secret'], callback=groupfinder, hashalg='sha512')
    ]
    authn_policy = MultiAuthenticationPolicy(policies)

    config = Configurator(settings=settings, root_factory=RootFactory, session_factory = my_session_factory)

    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)

    #Jinja:
    #config.add_translation_dirs('locale/')
    config.include('pyramid_jinja2')
    #Template locations
    config.add_jinja2_search_path('arhea:templates')
    #Supports updating objects in Jinja. Used in querysorter_m.jinja2
    config.add_jinja2_extension('jinja2.ext.do')


    #Static
    config.add_static_view(name='static', path='static', cache_max_age=3600)

    #Routes
    config.add_route('home', '/')

    #Security package sec include
    config.include('.app_sec.include')

    #Applications package apps include
    config.include('.app_apps.include')


    #Departments
    config.add_route('department_view', '/departments')
    config.add_route('department_view:page', '/departments/page/{page:\d+}')
    config.add_route('department_add', '/departments/add')
    config.add_route('department_edit', '/departments/{dep_id:\d+}/edit')
    #config.add_route('department_delete', '/departments/{dep_id:\d+}/del')

    #Employees
    config.add_route('employee_view', '/employees')
    config.add_route('employee_view:page', '/employees/page/{page:\d+}')
    config.add_route('employee_add', '/employees/add')
    config.add_route('employee_edit', '/employees/{emp_id:\d+}/edit')



    config.scan()
    return config.make_wsgi_app()
