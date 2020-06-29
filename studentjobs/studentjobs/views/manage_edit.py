
from studentjobs.security.acl import ACL
from studentjobs.models import DBSession,Users
from studentjobs.utilities.utility import has_interface
from studentjobs.views import BaseView
from studentjobs.views.manage_data import ManageData,Import
from pyramid.httpexceptions import HTTPFound
from pyramid.url import route_url
from pyramid.view import view_config
import transaction

class ManageDataEdit(ManageData):

    @view_config(route_name='manage_edit_data', renderer='../themes/templates/admin/data-edit.pt', permission=ACL.ADMINISTRATOR)
    def manage_edit_data(self):
        
        table = str(self.request.matchdict['table'])
        table_class = Import('studentjobs.models', table)
        id = self.request.matchdict['id']
        has_interface(table_class,'__scaffold__')
        
        if 'form.submit' in self.request.params or 'form.submit.list' in self.request.params:
            object = DBSession.query(table_class).filter(getattr(table_class,'id')==id).first()
            for p in self.request.params:
                name = p.replace('form.', '')  # all incoming form params are padding with this key
                if hasattr(object, name) and filter(lambda d: name in d, table_class.__scaffold__): # safety check
                    setattr(object, name, self.request.params.get(p))
            DBSession.flush()
            transaction.commit()
            if 'form.submit.list' in self.request.params:
                return HTTPFound(location=route_url('manage_list_data', self.request, table=table))
            
        object = DBSession.query(table_class).filter(getattr(table_class,'id')==id).first()
        html = self._element_generator(table_class.__scaffold__, object)
        self.set('allow_editing', getattr(table_class, '__allow_editing__', True))
        self.set('form',html)
        self.set('table', table)
        if table.endswith('ies'):
            self.set('table_singular', table[:-3] + 'y')
        elif table.endswith('ses'):
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
        
        
        