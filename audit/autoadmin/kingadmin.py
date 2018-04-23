#__author:zhang_lei

from audit import models
from audit.autoadmin.sites import site
from audit.autoadmin.base_admin import BaseKingAdmin
from audit.autoadmin.base_admin import BaseKingAdmin
class HostAdmin(BaseKingAdmin):
    list_display = ['id','hostname','ip_addr','port','enabled','idc']
    list_filters=['idc','enabled']
    search_fields = ['hostname']
    readonly_fields = ['hostname']
class UserProfileAdmin(BaseKingAdmin):
    list_display = ['id','last_login','email','is_staff']
    list_filters = [ 'is_staff']
    search_fields = ['username']
    readonly_fields = ['id']


class HostUserAdmin(BaseKingAdmin):
    list_display = ['id', 'username','auth_type']
    list_filters = ['auth_type']
    search_fields = ['username']
    
    readonly_fields = ['id']


class HostGroupAdmin(BaseKingAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    readonly_fields = ['id']


class BindHostAdmin(BaseKingAdmin):
	list_display = ['id','host', 'host_user']
 
	
site.register(models.SessionLog)
site.register(models.Host,HostAdmin)
site.register(models.BindHost,BindHostAdmin)
site.register(models.HostUser,HostUserAdmin)
site.register(models.IDC)
site.register(models.UserProfile,UserProfileAdmin)
site.register(models.HostGroup,HostGroupAdmin)
site.register(models.AuditLog)
site.register(models.TaskLogDetail)
site.register(models.Task)




















