
from studentjobs.security.core import RequestExtension,RootACL,groupfinder
from studentjobs.models import DBSession
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config,exc
import warnings

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    warnings.filterwarnings('ignore', '.*use_labels*.', category=exc.SAWarning)
    
    session_factory = UnencryptedCookieSessionFactoryConfig(str(settings['session_factory_key']))
    authorization_policy = ACLAuthorizationPolicy()
    authentication_policy = AuthTktAuthenticationPolicy(str(settings['authentication_policy_key']), callback=groupfinder)
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy,
                          request_factory=RequestExtension,
                          root_factory=RootACL,
                          session_factory=session_factory
    )
    
    config.add_static_view('themes', 'studentjobs:themes', cache_max_age=3600)
    
    # Public Stuff
    config.add_route('jobapp', '/')
    config.add_route('activity', '/activity')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('reset_password', '/reset_password')
    
    # Admin Stuff
    config.add_route('manage', '/manage')
    config.add_route('manage_users', '/manage/users')
    config.add_route('manage_users_add', '/manage/users/add')
    config.add_route('manage_user', '/manage/users/{id}')    
    config.add_route('manage_list_data', '/manage/data/{table}')
    config.add_route('manage_getlist_data', '/manage/data/{table}/list')
    config.add_route('manage_add_data', '/manage/data/{table}/add')
    config.add_route('manage_edit_data', '/manage/data/{table}/edit/{id}')
    config.add_route('manage_delete_data', '/manage/data/{table}/delete/{id}')
    config.add_route('manage_search', '/manage/search')
    config.add_route('manage_search_get', '/manage/search/get')
    config.add_route('manage_search_hired', '/manage/search/hired')
    config.add_route('manage_print', '/manage/print/{id}')
    
    
    #config.include('pyramid_mailer') 
    config.scan()
    return config.make_wsgi_app()

