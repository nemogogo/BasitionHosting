
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication


class MyAuthentication(BaseAuthentication):
	def authenticate(self, request):
		'''
		使用session检查是否登录
		:param request:
		:return:
		'''
		from django.contrib.sessions import models
		print('Authenticating---------')
		session_obj = models.Session.objects.filter(session_key=request._request.session.session_key)
		if not session_obj:
			print('yonghu 验证失败')
			raise exceptions.AuthenticationFailed('用户认证失败')
		session_obj.user = request._request.user
		return session_obj.user, session_obj
