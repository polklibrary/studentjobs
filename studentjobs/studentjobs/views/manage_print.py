
from studentjobs.security.acl import ACL
from studentjobs.models import DBSession, Users, Applications, States
from studentjobs.utilities.validators import Validators
from studentjobs.views import BaseView
from pyramid.view import view_config
from sqlalchemy import or_,and_,func
from datetime import date
import re, datetime, time

class ManagePrint(BaseView):

    @view_config(route_name='manage_print', renderer='../themes/templates/admin/print.pt', permission=ACL.REVIEWER)
    def manage_print(self):
        id = self.request.matchdict['id']
        
        
        if 'office.save' in self.request.params:
            state = int(self.request.params.get('office.state', 1))
            notes = self.request.params.get('office.notes', '')
            application = Applications.load(id=id)
            application.notes = notes
            application.state = state
            application.save(self.request)
        
        obj = DBSession.query(Applications).filter(Applications.id == id).first()
        self.set('data', obj)
        start_date = str(obj.start_date)
        self.set('data_start_date', start_date[0:4] + '-' + start_date[4:6]+ '-' + start_date[6:8])
        self.set('data_positions', obj.positions.replace(',','<br />'))
        self.set('data_reference_one', obj.reference_one.replace('\n','<br />'))
        self.set('data_reference_two', obj.reference_two.replace('\n','<br />'))
        self.set('data_employer_one', obj.employer_one.replace('\n','<br />'))
        self.set('data_employer_two', obj.employer_two.replace('\n','<br />'))
        self.set('data_monday', self.change_availability_to_readable(obj.monday_availability))
        self.set('data_tuesday', self.change_availability_to_readable(obj.tuesday_availability))
        self.set('data_wednesday', self.change_availability_to_readable(obj.wednesday_availability))
        self.set('data_thursday', self.change_availability_to_readable(obj.thursday_availability))
        self.set('data_friday', self.change_availability_to_readable(obj.friday_availability))
        self.set('data_saturday', self.change_availability_to_readable(obj.saturday_availability))
        self.set('data_sunday', self.change_availability_to_readable(obj.sunday_availability))
        
        self.set('states', States.loadAll())
        return self.response
        
    
    def change_availability_to_readable(self, data):
        output = ''
        time_ranges = data.split(';')
        for times in time_ranges:
            if times:
                t = times.split(',')
                output += t[0] + ' - ' + t[-1] + '<br />'
        return output
            
