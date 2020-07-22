from studentjobs.models import DBSession,Users,Config
from studentjobs.security.acl import ACL
from studentjobs.views import BaseView
from studentjobs.utilities.validators import Validators
from studentjobs.utilities.emailer import Emailer

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember,forget
from pyramid.url import route_url
from pyramid.view import view_config

import time, hashlib, transaction, ldap

class Login(BaseView):

    @view_config(route_name='login', renderer='../themes/templates/login.pt', permission=ACL.ANONYMOUS)
    def login(self):
        self.set('waiting_verify',False)
        self.set('issue', self.request.params.get('issue',''))
        if 'submit' in self.request.params:
            email = self.request.params.get('email',None)
            password = self.request.params.get('pass',None)
            goto = self.request.params.get('goto','')
            
            if email and password:
                user = Users.load(email=email)

                if user:
                
                    # Check against LDAP
                    if user.auth_type == Users.AUTH_LDAP:
                        if self.ldap_connect_and_check():
                            return HTTPFound(location=route_url('manage', self.request), headers=remember(self.request, user.id))
                        else:
                            self.set('issue','Incorrect credentials (Error=0A)')
                            
                    # Check against LOCAL
                    elif user.auth_type == Users.AUTH_LOCAL:
                        if user.password_failures >= int(Config.get('max_login_failures')):
                            user.password_failures += 1
                            self.set('issue','Your account is locked out.  Please contact your administrator.')
                        else:
                            now = (int(time.time())) - int(Config.get('password_mandatory_reset'))
                            if user.password_timestamp < now:
                                return HTTPFound(location=route_url('reset_password', self.request, _query={'mandatory':'1'}))
                            if user.validate_password(password):
                                user.password_failures = 0
                                if self.request.cookies.get('login_quick_key','0') == user.login_quick_key:
                                    if not goto:
                                        return HTTPFound(location=route_url('manage', self.request), headers=remember(self.request, user.id))
                                    else:
                                        return HTTPFound(location=goto, headers=remember(self.request, user.id))
                                else:
                                    user.gen_login_quick_key() # make new hash
                                    self.verify_email(user)
                                    DBSession.flush()
                                    transaction.commit()
                                    self.set('waiting_verify',True)
                            else:
                                user.password_failures += 1
                                self.set('issue','Incorrect credentials (Error=0B)')
                else:
                    self.set('issue','No user found')
            else:
                self.set('issue','No user or password provided')

        return self.response
    
    
    def ldap_connect_and_check(self):
        try:
            email = self.request.params.get('email','')
            password = self.request.params.get('pass','')
            
            # build a client
            ldap_client = ldap.initialize(self.settings('ldap.url','').strip())
            # perform a synchronous bind
            ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
            ldap_client.set_option(ldap.OPT_REFERRALS, 0)
            ldap_client.simple_bind_s(email, password)
            return True
            
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            return False
            
        except Exception as e:
            print "LDAP Error: " + str(e)
            return False
    
    
    def verify_email(self, user):
        hash = hashlib.sha256(user.login_quick_key + self.settings('hash_salt','fakesalt')).hexdigest()
        subject = 'Student Jobs Login Verification'
        
        link = self.request.application_url + '/verify?id=' + str(user.id) + '&hash=' + hash
        body = Config.get('twofactor_email_text', link)
        body = body.replace('$LINK', link)
        
        Emailer.send(self.request, user.email, subject, body)


class Verify(BaseView):

    @view_config(route_name='verify', permission=ACL.ANONYMOUS)
    def verify(self):
        id = self.request.params.get('id',0)
        hash = self.request.params.get('hash','')
        if id > 0:
            user = Users.load(id=id)
            if user:
                # Link timeout
                if int(time.time()) >= (user.login_quick_key_timestamp + int(Config.get('twofactor_timeout',300))):
                    return HTTPFound(route_url('login', self.request, _query=(('issue', 'TwoFactor link timed out.'),)), headers=forget(self.request), )

                # Hash check
                userhash = hashlib.sha256(user.login_quick_key + self.settings('hash_salt','fakesalt')).hexdigest()
                if userhash == hash:
                    response = HTTPFound(location=route_url('manage', self.request), headers=remember(self.request, user.id))
                    response.set_cookie('login_quick_key', user.login_quick_key, max_age=31536000)
                    return response
                else:
                    return HTTPFound(route_url('login', self.request, _query=(('issue', 'TwoFactor hash incorrect.'),)), headers=forget(self.request), )
        
        return HTTPFound(route_url('login', self.request, _query=(('issue', 'TwoFactor failed.'),)), headers=forget(self.request), )

        
        
        

class Logout(BaseView):

    @view_config(route_name='logout', permission=ACL.ANONYMOUS)
    def logout(self):    
        return HTTPFound(route_url('jobapp', self.request), headers=forget(self.request))
      
       
class ResetPassword(BaseView):

    @view_config(route_name='reset_password', renderer='../themes/templates/reset_password.pt', permission=ACL.ANONYMOUS)
    def reset_password(self):
        self.set('issue',None)
        self.set('password_help_text', Config.get('password_help_text'))
        self.set('mandatory',self.request.params.get('mandatory','0')=='1')
        
        if 'submit' in self.request.params:
            email = self.request.params.get('email','')
            password_current = self.request.params.get('password.current','')
            password_new = self.request.params.get('password.new','')
            password_repeat = self.request.params.get('password.repeat','')
            
            user = Users.load(email=email)
            
            if not user:
                self.set('issue','No email exists.')
                return self.response
                
            if not user.validate_password(password_current):
                self.set('issue','Your current password is incorrect.')
                return self.response
                
            if password_repeat != password_new:
                self.set('issue','Your new passwords do not match.')
                return self.response
                
            if not Validators.password(password_new, Config):
                self.set('issue','Your new password is not valid.')
                return self.response
                
            if user.check_old_passwords(password_new):
                self.set('issue','You have already used this password.')
                return self.response
                
            user.set_password(password_new)
            user.update_password_timestamp()
            return HTTPFound(location=route_url('login', self.request))

            
        return self.response
        