from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Host(models.Model):
    """储存主机列表"""
    hostname=models.CharField(max_length=64)
    ip_addr=models.GenericIPAddressField()
    port=models.SmallIntegerField(default=22)
    idc = models.ForeignKey("IDC",on_delete=models.CASCADE)
    enabled=models.BooleanField(default=False)
    class Meta:
        unique_together=('hostname','ip_addr')
    def __str__(self):
        return '%s@%s'%(self.hostname,self.ip_addr)

class BindHost(models.Model):
    """绑定主机和远程用户(主机账号)的对应关系"""
    host=models.ForeignKey('Host',on_delete=models.CASCADE)
    host_user=models.ForeignKey('HostUser',on_delete=models.CASCADE)
    class Meta:
        unique_together=('host','host_user')

    def __str__(self):
        return "%s %s" % (self.host, self.host_user)

class HostGroup(models.Model):
    """储存主机组"""
    name=models.CharField(max_length=64,unique=True)
    # hosts=models.ManyToManyField("Host")
    bind_hosts=models.ManyToManyField('BindHost')
    # hosts_to_remote_users=models.ManyToManyField("HostToRemoteUser")

    def __str__(self):
        return self.name


class HostUser(models.Model):
    """存储远程要管理的主机的账号信息"""

    auth_type_choices=((0,'ssh-password'),(1,'ssh-key'))
    auth_type=models.SmallIntegerField(choices=auth_type_choices,default=0)
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=128,blank=True,null=True)
    class Meta:
        unique_together=('auth_type','username','password')
    def __str__(self):
        return "%s" %(self.username)


class UserProfileManager(BaseUserManager):
    def create_user(self,email,name,password=None):
        """Create and saves a User with the given eamil,username
        and password"""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.is_staff= True
        user.set_password(password)
        user.save(using=self._db)

        return user
    def create_superuser(self,email,name,password):
        """Create and saves a superuser with the given email,username
        and password"""
        user=self.create_user(email,password=password,name=name,)
        user.is_superuser=True
        user.is_admin = True
        user.save(using=self._db)
        return user
class UserProfile(AbstractBaseUser,PermissionsMixin):
    """堡垒机账号"""
    email=models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        null=True
    )
    password = models.CharField(_('password'), max_length=128)
    username=models.CharField(max_length=64,verbose_name="姓名")
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    bind_hosts=models.ManyToManyField("BindHost",blank=True,null=True)
    host_groups=models.ManyToManyField("HostGroup",blank=True,null=True)
    objects = UserProfileManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        #The user is identified by their email address
        return self.email
    def get_short_name(self):
        #The user is identified by their email address
        return self.email
    def __str__(self):
        return str(self.email)

     

class IDC(models.Model):
    """机房信息"""
    name=models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.name

class AuditLog(models.Model):
    '''存储审计日志'''
    user=models.ForeignKey("UserProfile",verbose_name="堡垒机账号",null=True,blank=True,on_delete=models.CASCADE)
    bind_host=models.ForeignKey("BindHost",null=True,blank=True,on_delete=models.CASCADE)
    log_type_choices=((0,'login'),(1,'cmd'),(2,'logout'))
    log_type=models.SmallIntegerField(choices=log_type_choices,default=0)
    content=models.CharField(max_length=255,null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    def __str__(self):
        return "%s  %s"%(self.bind_host,self.content)

class SessionLog(models.Model):
    '''生成用户操作session id '''
    user = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    bind_host = models.ForeignKey('BindHost',on_delete=models.CASCADE)
    session_tag = models.CharField(max_length=128,default='n/a',unique=True)
    closed = models.BooleanField(default=False)
    cmd_count = models.IntegerField(default=0) #命令执行数量
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<id:%s user:%s bind_host:%s>' % (self.id,self.user.email,self.bind_host.host)
    class Meta:
        verbose_name = '审计日志'
        verbose_name_plural = '审计日志'

class Task(models.Model):
    """批量任务"""
    task_type_choices=(('cmd','批量命令'),('file-transfer','文件传输'))
    task_type=models.CharField(choices=task_type_choices,max_length=64,default=0)
    content=models.CharField(max_length=255,verbose_name='任务内容',blank=False,null=False,default=0)
    user=models.ForeignKey('UserProfile',on_delete=models.CASCADE,blank=False,null=False)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s-%s-%s"%(self.user,self.task_type,self.content)



class TaskLogDetail(models.Model):
    """存储批量任务的结果"""
    task=models.ForeignKey('Task',on_delete=models.CASCADE)
    bind_host=models.ForeignKey('BindHost',on_delete=models.CASCADE)
    result=models.TextField(verbose_name="任务执行结果")
    status_choices = ((0, 'initialized'), (1, 'sucess'), (2, 'failed'), (3, 'timeout'))
    status = models.SmallIntegerField(choices=status_choices, default=0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s %s" % (self.task, self.bind_host)






















