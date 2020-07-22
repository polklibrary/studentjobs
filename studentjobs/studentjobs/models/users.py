from sqlalchemy import Column,Integer,BigInteger,String,Unicode,Boolean,TIMESTAMP,ForeignKey,Table,Text
from sqlalchemy.orm import relation
from studentjobs.models import Base,DBSession,Model
import os, transaction, datetime, time, hashlib, uuid


class Users(Base,Model):
    __tablename__ = 'users'
    
    AUTH_LOCAL = 0
    AUTH_LDAP = 1

    id = Column(Integer, primary_key=True)
    auth_type = Column(Integer)
    email = Column(Unicode(25), unique=True)
    password = Column(Unicode(255))
    group = Column(Unicode(25))
    login_quick_key = Column(Unicode(255))
    login_quick_key_timestamp = Column(BigInteger(unsigned=True))
    password_failures = Column(Integer)
    session_timestamp = Column(BigInteger(unsigned=True))
    password_timestamp = Column(BigInteger(unsigned=True))
    password_history = Column(Text)
    
    def __init__(self, **kwargs):
        from studentjobs.security.acl import ACL
        self.auth_type = kwargs.get('auth_type', self.AUTH_LOCAL)
        self.email = kwargs.get('email','')
        self.set_password(kwargs.get('password',None))
        self.group = kwargs.get('group', ACL.AUTHENTICATED)
        self.gen_login_quick_key()
        self.update_session_timestamp()
        self.update_password_timestamp()
        self.password_history += self.password
        self.password_failures = 0

    def gen_login_quick_key(self):
        self.update_login_quick_key_timestamp()
        self.login_quick_key = hashlib.sha256(str(uuid.uuid4())).hexdigest()
        
    def check_old_passwords(self, password):
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password
        password_hash = hashlib.sha256(password_8bit).hexdigest()
        return password_hash in self.password_history

    def set_password(self, password):
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password
            
        password_hash = hashlib.sha256(password_8bit).hexdigest()

        if self.password_history:
            self.password_history += '|' + password_hash
        else:
            self.password_history = password_hash
            
        self.password = password_hash

    def validate_password(self, password):
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password
        password_hash = hashlib.sha256(password_8bit).hexdigest()
        return self.password == password_hash and self.password != None
        

    def add_user(self):
        if self.__class__.__name__ == 'Users':
            DBSession.add(self)
            transaction.commit()
    
    
    def update_session_timestamp(self):
        self.session_timestamp = int(time.time())
        
    def update_password_timestamp(self):
        self.password_timestamp = int(time.time())
        
    def update_login_quick_key_timestamp(self):
        self.login_quick_key_timestamp = int(time.time())
        
    
    
class GuestUser(object):
    id = 0
    user = 'Guest'
    password = 'Guest'
    group = 'Anonymous'
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    