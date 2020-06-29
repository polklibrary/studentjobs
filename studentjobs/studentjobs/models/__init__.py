from studentjobs.security.acl import ACL
from studentjobs.security.decorators import protected
from sqlalchemy import or_
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension
import os,transaction,datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Model(object):
    
    def insert(self, request):
        DBSession.add(self)
        DBSession.flush()
        tmp = self.id
        transaction.commit()
        return tmp
    
    @protected([ACL.AUTHENTICATED,ACL.REVIEWER,ACL.ADMINISTRATOR])
    def save(self, request):
        DBSession.flush()
        transaction.commit()

    @protected([ACL.REVIEWER,ACL.ADMINISTRATOR])
    def remove(self):
        DBSession.delete(self)
        transaction.commit()
        
    @protected([ACL.ADMINISTRATOR])
    def remove_admin_only(self, request):
        DBSession.delete(self)
        transaction.commit()
        
    @classmethod
    def _load(cls,**kwargs):
        """ Main Loader """
        
        query = DBSession.query(cls)
        
        for key in kwargs:
            if key not in ['order','like','offset','limit']:
                query = query.filter(getattr(cls,key)==kwargs[key])
        if 'like' in kwargs:
            for key,value in kwargs.get('like').items():
                query = query.filter(getattr(cls,key).like('%'+value+'%'))
        if 'order' in kwargs:
            query = query.order_by(kwargs.get('order'))
        if 'offset' in kwargs:
            query = query.offset(kwargs.get('offset'))
        if 'limit' in kwargs:
            query = query.limit(kwargs.get('limit'))

        return query
    
    @classmethod
    def load(cls,**kwargs):
        return cls._load(**kwargs).first()
        
    @classmethod
    def loadAll(cls,**kwargs):
        return cls._load(**kwargs).all()
        
    @classmethod
    def TotalCount(cls,**kwargs):
        return cls._load(**kwargs).count()
        
        
        

# Import Shortcuts
from studentjobs.models.applications import Applications
from studentjobs.models.config import Config
from studentjobs.models.positions import Positions
from studentjobs.models.states import States
from studentjobs.models.users import Users,GuestUser
