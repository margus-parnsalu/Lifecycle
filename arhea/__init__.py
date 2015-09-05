"""
Application for system lifecycle management
Main package that includes app_* extensions
"""
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
from .utils.custom_jinja_filters import datetimeformat

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    #Session factory (CSRF)
    my_session_factory = SignedCookieSessionFactory(settings['session.secret'])

    #SqlAlchemy:
    engine = engine_from_config(settings, 'sqlalchemy.default.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    engine2 = engine_from_config(settings, 'sqlalchemy.ea.',
                                 pool_size=settings.get('sqla_ea_pool_size', 5),
                                 max_overflow=settings.get('sqla_ea_max_overflow', 20),
                                 pool_recycle=settings.get('sqla_ea_pool_recycle', 3600))
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
    #Register custom filter in Jinja
    config.commit()
    config.get_jinja2_environment().filters['datetimeformat'] = datetimeformat


    #Static
    config.add_static_view(name='static', path='static', cache_max_age=3600)

    #Routes
    config.add_route('home', '/')

    #Security package sec include
    config.include('.app_sec.include')

    #Applications package apps include
    config.include('.app_apps.include')

    #HR package apps include
    config.include('.app_hr.include')


    config.scan()
    return config.make_wsgi_app()
