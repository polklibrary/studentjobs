from studentjobs.security.acl import ACL
from studentjobs.models import Users, Config, Applications, Positions
from studentjobs.utilities.validators import Validators
from studentjobs.views import BaseView
from pyramid.view import view_config
import datetime

class JobAppView(BaseView):

    @view_config(route_name='jobapp', renderer='../themes/templates/jobapp.pt', permission=ACL.ANONYMOUS)
    def jobapp(self):
        self.set('completed', False)
        
        positions_data = []
        objs = Positions.loadAll(order='name asc')
        for obj in objs:
            positions_data.append({
                'id':obj.id,
                'name':obj.name,
                'title':obj.title,
            })
        self.set('positions', positions_data)
        
        
        if 'applicant.submit' in self.request.params:
            name =  Validators.safe_text(self.request.params.get('applicant.name',''))
            email = self.request.params.get('applicant.email','')
            local_address =  Validators.safe_text(self.request.params.get('applicant.local_address',''))
            home_address =  Validators.safe_text(self.request.params.get('applicant.home_address',''))
            work_study = self.request.params.get('applicant.work_study','')
            work_study_amount = self.request.params.get('applicant.work_study_amount','')
            graduation_term = self.request.params.get('applicant.graduation_term','')
            graduation_year = self.request.params.get('applicant.graduation_year','')
            work_hours_range = self.request.params.get('applicant.work_hours_range','')
            start_date = self.request.params.get('applicant.start_date','')
            positions = self.request.params.getall('applicant.positions')
            service_experience =  Validators.safe_text(self.request.params.get('applicant.service_experience',''))
            tech_experience =  Validators.safe_text(self.request.params.get('applicant.tech_experience',''))
            library_assets =  Validators.safe_text(self.request.params.get('applicant.library_assets',''))
            reference_one_name =  Validators.safe_text(self.request.params.get('reference.one.name',''))
            reference_one_phone = self.request.params.get('reference.one.phone','')
            reference_one_acquainted =  Validators.safe_text(self.request.params.get('reference.one.acquainted',''))
            reference_two_name =  Validators.safe_text(self.request.params.get('reference.two.name',''))
            reference_two_phone = self.request.params.get('reference.two.phone','')
            reference_two_acquainted =  Validators.safe_text(self.request.params.get('reference.two.acquainted',''))
            employer_one_name =  Validators.safe_text(self.request.params.get('employer.one.name',''))
            employer_one_phone = self.request.params.get('employer.one.phone','')
            employer_one_leave =  Validators.safe_text(self.request.params.get('employer.one.leave',''))
            employer_two_name =  Validators.safe_text(self.request.params.get('employer.two.name',''))
            employer_two_phone = self.request.params.get('employer.two.phone','')
            employer_two_leave =  Validators.safe_text(self.request.params.get('employer.two.leave',''))
            availability_monday = self.request.params.get('availability.monday','')
            availability_tuesday = self.request.params.get('availability.tuesday','')
            availability_wednesday = self.request.params.get('availability.wednesday','')
            availability_thursday = self.request.params.get('availability.thursday','')
            availability_friday = self.request.params.get('availability.friday','')
            availability_saturday = self.request.params.get('availability.saturday','')
            availability_sunday = self.request.params.get('availability.sunday','')
            
            if positions:
                positions = ', '.join(positions)
    
            application = Applications(
                name = name, 
                email = email, 
                local_address = local_address,
                home_address = home_address,
                work_study = Validators.bool(work_study),
                work_study_amount = int(work_study_amount),
                expected_graduation_term = graduation_term,
                expected_graduation_year = int(graduation_year),
                hours_per_week = work_hours_range,
                start_date = int(filter(str.isdigit, str(start_date))),
                positions = positions,
                service_experience = service_experience,
                technology_experience = tech_experience,
                library_experience = library_assets,
                reference_one = self.reference_fmt(reference_one_name, reference_one_phone, reference_one_acquainted),
                reference_two = self.reference_fmt(reference_two_name, reference_two_phone, reference_two_acquainted),
                employer_one = self.employer_fmt(employer_one_name, employer_one_phone, employer_one_leave),
                employer_two = self.employer_fmt(employer_two_name, employer_two_phone, employer_two_leave),
                monday_availability = self.time_range_creator(availability_monday),
                tuesday_availability = self.time_range_creator(availability_tuesday),
                wednesday_availability = self.time_range_creator(availability_wednesday),
                thursday_availability = self.time_range_creator(availability_thursday),
                friday_availability = self.time_range_creator(availability_friday),
                saturday_availability = self.time_range_creator(availability_saturday),
                sunday_availability = self.time_range_creator(availability_sunday),
            )
            application.insert(self.request)
            self.set('completed', True)
            print "Creating Application: " + str(email)
            
            
        return self.response
        
        
        
        
    def reference_fmt(self, name, phone, acquainted):  
        return name + '\n' + phone + '\n' + acquainted   
        
    def employer_fmt(self, name, phone, leave):  
        return name + '\n' + phone + '\n' + leave   
        
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
                    
                final_result += result + ';'
                
        return final_result
        
    
    
    
    
    