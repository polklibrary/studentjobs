from sqlalchemy import Column,Integer,BigInteger,String,Unicode,Boolean,TIMESTAMP,ForeignKey,Table,Text
from sqlalchemy.orm import relation
from studentjobs.models import Base,DBSession,Model
import os, transaction, datetime, time


class Applications(Base,Model):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(128))
    email = Column(Unicode(25), unique=True)
    local_address = Column(Unicode(255))
    home_address = Column(Unicode(255))
    work_study = Column(Boolean)
    work_study_amount = Column(Integer)
    expected_graduation_term = Column(Unicode(32))
    expected_graduation_year = Column(Integer)
    hours_per_week = Column(Unicode(32))
    start_date = Column(Integer)
    positions = Column(Text)
    service_experience = Column(Text)
    technology_experience = Column(Text)
    library_experience = Column(Text)
    reference_one = Column(Text)
    reference_two = Column(Text)
    employer_one = Column(Text)
    employer_two = Column(Text)
    monday_availability = Column(Text)
    tuesday_availability = Column(Text)
    wednesday_availability = Column(Text)
    thursday_availability = Column(Text)
    friday_availability = Column(Text)
    saturday_availability = Column(Text)
    sunday_availability = Column(Text)
    state = Column(Integer)
    created = Column(BigInteger)
    
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name','')
        self.email = kwargs.get('email','')
        self.local_address = kwargs.get('local_address','')
        self.home_address = kwargs.get('home_address','')
        self.work_study = kwargs.get('work_study',False)
        self.work_study_amount = kwargs.get('work_study_amount',0)
        self.expected_graduation_term = kwargs.get('expected_graduation_term','')
        self.expected_graduation_year = kwargs.get('expected_graduation_year',1999)
        self.hours_per_week = kwargs.get('hours_per_week','')
        self.start_date = kwargs.get('start_date',29991231)
        self.positions = kwargs.get('positions','')
        self.service_experience = kwargs.get('service_experience','')
        self.technology_experience = kwargs.get('technology_experience','')
        self.library_experience = kwargs.get('library_experience','')
        self.reference_one = kwargs.get('reference_one','')
        self.reference_two = kwargs.get('reference_two','')
        self.employer_one = kwargs.get('employer_one','')
        self.employer_two = kwargs.get('employer_two','')
        self.monday_availability = kwargs.get('monday_availability','')
        self.tuesday_availability = kwargs.get('tuesday_availability','')
        self.wednesday_availability = kwargs.get('wednesday_availability','')
        self.thursday_availability = kwargs.get('thursday_availability','')
        self.friday_availability = kwargs.get('friday_availability','')
        self.saturday_availability = kwargs.get('saturday_availability','')
        self.sunday_availability = kwargs.get('sunday_availability','')
        self.state = kwargs.get('state',1)
        self.created = long(time.time())

