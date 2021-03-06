from sqlalchemy import Column,Integer,BigInteger,String,Unicode,Boolean,TIMESTAMP,ForeignKey,Table,Text
from sqlalchemy.orm import relation
from hashlib import sha1
from studentjobs.models import Base,DBSession,Model

import os,transaction,datetime,re


class States(Base,Model):
    __tablename__ = 'states'

    __scaffold__ = [{'id': { 'widget': 'input', 'label': 'ID', 'attributes': {'type':'text', 'disabled':'true'} } },
                    {'name': { 'widget': 'input', 'label': 'Name', 'attributes': {'type':'text'} } },
                    {'notes': { 'widget': 'input', 'label': 'Note', 'attributes': {'type':'text'} } },
    ]
    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(55))
    notes = Column(Unicode(255))
    
    def __init__(self, **kwargs):
        self.name = kwargs.get('name','')
        self.notes = kwargs.get('notes','')


    
    