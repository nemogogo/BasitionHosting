from rest_framework.throttling import BaseThrottle,SimpleRateThrottle
import time
VisitRecord={}

class VisitThrottle(BaseThrottle):
	def __init__(self):
		self=history=None
	def wait(self):
		return 60-(time.time()-self.history[-1])
	
	def allow_request(self,request,view):
		'''
		限制访问频率
		:param request:
		:param view:
		:return:
		'''
		remote_addr = self.get_ident(request)
		print('Throttling-----------')
		ctime = time.time()
		if remote_addr not in VisitRecord:
			VisitRecord[remote_addr] = [ctime, ]
			return True
		history = VisitRecord[remote_addr]
		self.history=history
		while history and history[-1]<ctime-60:
			history.pop()
			
		if len(history)<3:
			history.insert(0,ctime)
			return True
		 
	
  
class MyThrottle(SimpleRateThrottle):
	scope = 'audit'
	def get_cache_key(self, request, view):
		return self.get_ident(request)
  

