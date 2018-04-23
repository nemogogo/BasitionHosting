#__author:zhang_lei

from audit.autoadmin.base_admin import BaseKingAdmin

class AdminSite(object):
    '''
    注册admin表的类
    '''
    def __init__(self):
        self.enabled_admins={}

    def register(self,model_class,admin_class=None):
        """注册admin表
        """
        if not admin_class:
            admin_class=BaseKingAdmin()
        else:
            admin_class=admin_class()
        admin_class.model=model_class
        app_name=model_class._meta.app_label
        model_name=model_class._meta.model_name
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name]={}
        self.enabled_admins[app_name][model_name]=admin_class

site=AdminSite()