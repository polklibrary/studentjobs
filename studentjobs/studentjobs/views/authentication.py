from studentjobs.models import Users,Config
from studentjobs.security.acl import ACL
from studentjobs.views import BaseView
from studentjobs.utilities.validators import Validators

from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember,forget
from pyramid.url import route_url
from pyramid.view import view_config

import time

class Login(BaseView):

    @view_config(route_name='login', renderer='../themes/templates/login.pt', permission=ACL.ANONYMOUS)
    def login(self):
        self.set('issue','')
        if 'submit' in self.request.params:
            email = self.request.params.get('email',None)
            password = self.request.params.get('pass',None)
            goto = self.request.params.get('goto','')
            if email and password:
                user = Users.load(email=email)
                if user:
                    if user.password_failures >= int(Config.get('max_login_failures')):
                        user.password_failures += 1
                        self.set('issue','Your account is locked out.  Please contact your administrator.')
                    else:
                        now = (int(time.time())) - int(Config.get('password_mandatory_reset'))
                        if user.password_timestamp < now:
                            return HTTPFound(location=route_url('reset_password', self.request, _query={'mandatory':'1'}))
                        if user.validate_password(password):
                            user.password_failures = 0
                            if not goto:
                                return HTTPFound(location=route_url('manage', self.request), headers=remember(self.request, user.id))
                            else:
                                return HTTPFound(location=goto, headers=remember(self.request, user.id))
                        else:
                            user.password_failures += 1
                            self.set('issue','Incorrect credentials')
                else:
                    self.set('issue','No user found')
            else:
                self.set('issue','No user or password provided')

        return self.response
        

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
        