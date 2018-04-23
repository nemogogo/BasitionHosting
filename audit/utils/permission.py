from rest_framework.permissions import BasePermission

from rest_framework import exceptions
from audit.utils import throttle
class MyPermission(BasePermission):
	perms_map = {
		'GET':['%(app_label)s.change_%(model_name)s'],
		'OPTIONS': ['%(app_label)s.change_%(model_name)s'],
		'HEAD': [],
		'POST': ['%(app_label)s.add_%(model_name)s'],
		'PUT': ['%(app_label)s.change_%(model_name)s'],
		'PATCH': ['%(app_label)s.change_%(model_name)s'],
		'DELETE': ['%(app_label)s.delete_%(model_name)s'],
	}
	message="你没有此Model的权限"
	
	def get_required_permissions(self, method, **kwargs):
		"""
		Given a model and an HTTP method, return the list of permission
		codes that the user is required to have.
		"""
		kwargs = {
			'app_label': kwargs['app_label'],
			'model_name': kwargs['model_name'],
		}
		if method not in self.perms_map:
			exceptions.MethodNotAllowed(method)
		
		return [perm %kwargs for perm in self.perms_map[method]]
	def has_permission(self,request,view):
		'''
		用django自带的权限系统实现权限控制
		:param request:
		:param view:
		:return:
		'''
		print('permission---------------request.method',request.method)
		app_label,model_name=request.path.strip('/').split('/')[0:2]
		print(request._request.META)
		user = getattr(request._request, 'user', None)
 
		perm=self.get_required_permissions(request.method.upper(),app_label=app_label,model_name=model_name)
		if not user:
			return False
		#根据app_label,model_name制定序列化类
		from audit.autoadmin import sites
		from audit.utils.serializer import create_serializer
		model_admin = sites.site.enabled_admins[app_label][model_name]
		view.model_admin=model_admin
		view.app_name=app_label
		view.table_name = model_name
		view.serializer_class= create_serializer(model_admin.model, model_admin.list_display)
		#根据用户类型设定访问频率限制
		if user.is_superuser:
			view.throttle_classes = [throttle.MyThrottle,]
		if perm:
			if user.has_perms(perm):
				return True
			
		return False
			
			

