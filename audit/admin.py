from django.contrib import admin
from audit import models

# Register your models here.

admin.site.register(models.AuditLog)
admin.site.register(models.BindHost)
admin.site.register(models.Host)
admin.site.register(models.HostGroup)
admin.site.register(models.HostUser)
admin.site.register(models.IDC)
admin.site.register(models.SessionLog)
admin.site.register(models.Task)
admin.site.register(models.TaskLogDetail)
admin.site.register(models.UserProfile)
