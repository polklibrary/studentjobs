
from studentjobs.security.acl import ACL
from studentjobs.models import DBSession,Users
from studentjobs.utilities.utility import has_interface
from studentjobs.utilities.validators import Validators
from studentjobs.views import BaseView
from studentjobs.views.manage_data import ManageData,Import
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.view import view_config
import transaction

class ManageDataAdd(ManageData):

    @view_config(route_name='manage_add_data', renderer='../themes/templates/admin/data-add.pt', permission=ACL.ADMINISTRATOR)
    def manage_add_data(self):
        
        table = str(self.request.matchdict['table'])
        table_class = Import('studentjobs.models', table)
        has_interface(table_class,'__scaffold__')
        
        if 'form.submit' in self.request.params or 'form.submit.another' in self.request.params:
            object = table_class()
            
            for p in self.request.params:
                name = p.replace('form.', '')  # all incoming form params are padding with this key
                if hasattr(object, name) and filter(lambda d: name in d, object.__scaffold__): # safety check
                    setattr(object, name, Validators.safe_text(self.request.params.get(p)))
            DBSession.add(object)
            DBSession.flush()
            transaction.commit()
            if 'form.submit' in self.request.params:
                return HTTPFound(location=route_url('manage_list_data', self.request, table=table))
                
            
        html = self._element_generator(table_class.__scaffold__, table_class())
        self.set('form',html)
        self.set('table', table)
        if table.endswith('ies'):
            self.set('table_singular', table[:-3] + 'y')
        elif table.endswith('es'):
            self.set('table_singular', table[:-2])
        elif table.endswith("'s"):
            self.set('table_singular', table[:-2])
        elif table.endswith('s'):
            self.set('table_singular', table[:-1])
        else:
            self.set('table_singular', table)
            
            
        self.set('friendly_table', getattr(table_class, '__tablelabel__', table))
        self.set('friendly_table_singular', getattr(table_class, '__tablelabel__', table)[:-1])
        
        return self.response
        
        
        