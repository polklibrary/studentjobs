from email.utils import parseaddr
import re, datetime, urllib

class Validators(object):

    # @classmethod
    # def alias(cls,alias):
        # """ TODO: improve later """
        # return (len(alias) > 3 and len(alias) < 15 and re.match('^[A-Za-z0-9_-]+$', alias) is not None)


    @classmethod
    def email_in_password(cls, password, email):
        name = email.split('@')[0]
        return name in password

    @classmethod
    def password(cls, password, Config):
        passes = True
        if len(password) < int(Config.get('password_min_length')):
            passes = False
        if len(password) > 64:
            passes = False
        regs = Config.get('password_regex').replace('\r','').split('\n')
        for r in regs:
            if not re.search(r, password):
                passes = False
        return passes

    @classmethod
    def email(cls,email):
        e = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
        return (len(e.findall(email)) > 0)
        #return (parseaddr(email)[1] != '')

    @classmethod
    def sanatize_textsafe(cls,text):
        """ Remove all types of spaces """
        return re.sub('[<>/+{}&@~`]','',text)
        
    @classmethod
    def sanatize(cls,text):
        """ Remove all types of spaces """
        return text.replace(' ','')
        
        
    @classmethod
    def safe_text(cls,text):
        """ Safe text for saving into database """
        text = text.replace(u"\u2018", u"'").replace(u"\u2019", u"'")
        text = text.replace(u"\u201c", u'"').replace(u"\u201d", u'"')
        text = text.replace(u"\u2013", u'-')
        return text.encode('ascii', errors='ignore')
        
    @classmethod
    def safe_htmltext(cls, text):
        """ Safe text for saving into database """        
        text = text.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
        return text
        
        
    @classmethod
    def is_acl(cls,group):
        group = cls.sanatize_textsafe(group)
        return group == 'Administrator' or group == 'Anonymous' or group == 'Reviewer' or group == 'Authenticated'
        
    @classmethod
    def bool(cls,o):
        if isinstance(o, str) or isinstance(o, unicode):
            return o.lower() in ['true','t','y','yes','1','on']
        elif isinstance(o, int):
            return (o > 0)
        elif isinstance(o, list):
            return (len(o) > 0)
        else:
            return bool(o)


    re.search('\d+[A-Z]+', 'eest1234')
    re.search('\d+', 'Dest1234')