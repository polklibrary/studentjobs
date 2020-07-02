from studentjobs.models import DBSession, Config
from pyramid_mailer import get_mailer
from pyramid_mailer.message import Attachment,Message

class Emailer(object):

    @classmethod
    def send(cls, request, to, subject, body):
        try:
            sys_email = Config.get('system_email')
            if not isinstance(to, list):
                to = to.split(',')
            
            message = Message(subject=subject,
                              sender=sys_email,
                              recipients=to,
                              body=body)
            mailer = get_mailer(request)
            mailer.send(message)
            
            return True
        except Exception as e:
            print "ERROR" + str(e)
            return False