
from studentjobs.security.acl import ACL
from studentjobs.models import DBSession, Users, Applications, Positions
from studentjobs.utilities.validators import Validators
from studentjobs.views import BaseView
from pyramid.view import view_config
from sqlalchemy import or_,and_,func
from datetime import date
import re, datetime, time

class ManageSearch(BaseView):

    @view_config(route_name='manage_search', renderer='../themes/templates/admin/search.pt', permission=ACL.REVIEWER)
    def manage_search(self):
        self.set('positions', Positions.loadAll(order='name asc'));
        return self.response
        
        
    @view_config(route_name='manage_search_hired', renderer='json', permission=ACL.REVIEWER)
    def manage_search_hired(self):
        id = int(self.request.params.get('id',0))
        current_state = 0
        if id > 0:
            application = Applications.load(id=id)
            if application.state == 1:
                application.state = 2
            else:
                application.state = 1
            current_state = application.state
            application.save(self.request)
    
        return {'state': current_state}
        
    @view_config(route_name='manage_search_get', renderer='json', permission=ACL.REVIEWER)
    def manage_search_get(self):
    
        name = self.request.params.get('search.name', '')
        email = self.request.params.get('search.email', '')
        query = None
        if name:
            query = DBSession.query(Applications).filter(Applications.name.like('%' + name + '%'))
        elif email: 
            query = DBSession.query(Applications).filter(Applications.email.like('%' + email + '%'))
        else:
            query = DBSession.query(Applications)

            # WORK STUDY
            if Validators.bool(self.request.params.get('search.workstudy','false')):
                query = query.filter(Applications.work_study == True)
            
            # DAY 
            start_date = int(re.sub('[^0-9]', '', self.request.params.get('search.start_date',0)))
            query = query.filter(Applications.start_date >= start_date)
            
            # POSITIONS
            positions_andor = self.request.params.get('search.positions.andor','or')
            positions = self.request.params.get('search.positions','').split(',')
            clauses_positions = []
            for position in positions:
                clauses_positions.append( (Applications.positions.like('%' + position + '%')) )
            if positions_andor == 'or':
                query = query.filter(or_(*clauses_positions))
            else:
                query = query.filter(and_(*clauses_positions))
            

            # Day And Time Check
            availability_andor = self.request.params.get('search.availability.andor','and')
            clauses_daytime = []
            for i in range(0,10):
                times = self.time_range_creator(self.request.params.get('search.time.' + str(i),''))
                days = self.request.params.get('search.day.' + str(i), '').split(',')
                if times:
                    for day in days:
                        if day:
                            clauses_daytime.append( getattr(Applications, day.lower() + '_availability').like('%' + times + '%') )
            if clauses_daytime: 
                if availability_andor == 'or':
                    query = query.filter(or_(*clauses_daytime))
                else:
                    query = query.filter(and_(*clauses_daytime))
                
        if query:
            count = query.count() # get total number of records
            objs = query.all()
            objs = query.order_by('id desc')
        else:
            count = 0
            objs = []
            
        results = {"recordsTotal": count,
                   "recordsFiltered": count,
                   "data": []
        }
        
        LIMIT = 150
        for obj in objs:
            results['data'].append({
                'id': obj.id,
                'name': obj.name,
                'email': obj.email,
                'local_address': obj.local_address,
                'home_address': obj.home_address,
                'work_study_amount': obj.work_study_amount,
                'expected_graduation_term':obj.expected_graduation_term,
                'expected_graduation_year':obj.expected_graduation_year,
                'hours_per_week':obj.hours_per_week,
                'text_preview':obj.service_experience[0:LIMIT] + '...\n---\n' + obj.technology_experience[0:LIMIT] + '...\n---\n' + obj.library_experience[0:LIMIT] + '...',
                'state':obj.state,
            })
                
        return results
        
        
    def time_range_creator(self, time_ranges):
        final_result = ''
        for time_range in time_ranges.split(','):
            if time_range:
                times = time_range.split(' - ')
                start_time = times[0]
                end_time = times[1]
                start = datetime.datetime.strptime('Dec 31 2010  ' + start_time, '%b %d %Y %I:%M %p')
                end = datetime.datetime.strptime('Dec 31 2010  ' + end_time, '%b %d %Y %I:%M %p')
                
                result = start.strftime('%I:%M%p')
                
                infinite_loop_preventor = 0
                while infinite_loop_preventor < 100:
                    infinite_loop_preventor+=1
                    
                    start = start + datetime.timedelta(minutes=15)
                    result += ',' + start.strftime('%I:%M%p')
                    if start >= end:
                        break;
                    
                final_result += result  # STOP CHANGED
                
        return final_result
        