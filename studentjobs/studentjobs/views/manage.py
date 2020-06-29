
from studentjobs.security.acl import ACL
from studentjobs.models import DBSession, Users, Applications, Config
from studentjobs.views import BaseView
from pyramid.view import view_config
from sqlalchemy import or_,and_,func

from datetime import date
import time, transaction

class Manage(BaseView):

    @view_config(route_name='manage', renderer='../themes/templates/admin/manage.pt', permission=ACL.REVIEWER)
    def manage(self):
    
        self.set('application_total', Applications.TotalCount())
        self.set('application_hired', len(Applications.loadAll(state=2)))
        self.set('application_open', len(Applications.loadAll(state=1)))
        
        purge_seconds = int(Config.get('retention_in_seconds'))
        purge_days = purge_seconds / 86400
        self.set('purge_days', purge_days)
        
        now = long(time.time())
        purge_timestamp = now - purge_seconds
        query = DBSession.query(Applications).filter(Applications.created<=purge_timestamp)
        results = query.all()
        for result in results:
            DBSession.delete(result)
        transaction.commit()
        
        
        return self.response
        
        