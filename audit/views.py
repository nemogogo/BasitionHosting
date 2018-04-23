from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from audit import models
from django.contrib.auth import login,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from audit.autoadmin import sites
from rest_framework import serializers
from rest_framework.views import APIView
from audit.autoadmin import set_up
from django.views import View
from audit.utils.serializer import create_serializer
import json
from rest_framework.pagination import PageNumberPagination
from audit.utils.view_contains import table_filter,table_search
from backend.multitask import MultiTaskManager
from audit.autoadmin.forms import creat_model_form
# Create your views here.
def acc_login(request):
    '''
    用户登陆
    :param request:
    :return:
    '''
    error_msg = ''

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = auth.authenticate(username=username, password=password)
        if user:
            login(request, user)
            request.user=user
            return HttpResponseRedirect(request.GET.get('next') if request.GET.get('next') else '/audit/index')
        else:
            error_msg = "Wrong username or password!"
    return render(request, 'login.html', {'error_msg': error_msg})

def register(request):
    from audit import forms as audit_form
    userobj = audit_form.UserCreationForm()
    if request.method=='POST':
        userobj=audit_form.UserCreationForm(request.POST)
        if userobj.is_valid():
            userobj.clean()
            userobj.save(commit=True)
            return redirect('/audit/login/')

    return render(request,'register.html',{'form':userobj})
  
@login_required(login_url='/audit/login')
def index(request):
	for app_name,model_name in sites.site.enabled_admins.items():
		print(app_name)
		
	return render(request,'index.html',{'site':sites.site,})

def acc_logout(request):
    logout(request)
    return redirect('/audit/login')

def web_ssh(request):
    return render(request, 'web_ssh.html')

class TableView(APIView):
 
	def get(self,request,*args,**kwargs):
		app_name,table_name=args
		model_admin=sites.site.enabled_admins[app_name][table_name]
		# auto_serializer=create_serializer(model_admin.model,model_admin.list_display)
		query_set=model_admin.model.objects.all()
		query_set, filter_condtions = table_filter(request, model_admin)
		query_set = table_search(request, model_admin, query_set)
		pg=PageNumberPagination()
		pg_set=pg.paginate_queryset(request=request,queryset=query_set,view=self)
		ser=self.serializer_class(instance=pg_set,many=True)
		print(pg.page.number)
		print(pg.get_next_link())
	 
	 
		data=ser.data
		if data:
			fields=data[0].keys()
	 
		return  render(request,'tables/table_detail.html',locals())


@login_required
def batch_task(request):


    return render(request,'task/host_manager.html')
		
	
@login_required
def batch_task_manager(request):
 
    task_result_obj = MultiTaskManager(request)

    response={
        'task_id':task_result_obj.task_obj.id,
        'selected_hosts': list(task_result_obj.task_obj.tasklogdetail_set.all().values('id',
                                                       'bind_host__host__ip_addr',
                                                       'bind_host__host__hostname',
                                                       'bind_host__host_user__username')
                                )
    }

    return HttpResponse(json.dumps(response))
@login_required
def task_result(request):
    task_id = request.GET.get('task_id')

    sub_tasklog_objs = models.TaskLogDetail.objects.filter(task_id=task_id)

    #log_data = sub_tasklog_objs.values('id','status','result','date')
    log_data = list(sub_tasklog_objs.values('id','status','result'))

    return HttpResponse(json.dumps(log_data))

@login_required
def file_transfer(request):


    return render(request,'task/file_transfer.html')
from rest_framework.viewsets import ModelViewSet


class TableView1(ModelViewSet):
	pagination_class = PageNumberPagination
 
	def get_queryset(self):
	 
		self.queryset = self.model_admin.model.objects.all()
		return self.queryset
	
	def list(self, request, *args, **kwargs):
		app_name=self.app_name
		table_name=self.table_name
		if args[2]:
			setattr(self.model_admin, 'is_add_form',True)
			model_form = creat_model_form(request, self.model_admin)
			form_obj = model_form()
			return render(request,'tables/table_add.html',locals())
		query_set = self.filter_queryset(self.get_queryset())
		model_admin = sites.site.enabled_admins[self.app_name][self.table_name]
		query_set, filter_condtions = table_filter(request, model_admin)
		query_set = table_search(request, model_admin, query_set)
		pg =self.pagination_class()
		page = pg.paginate_queryset(request=request,queryset=query_set,view=self)
		ser = self.serializer_class(instance=page, many=True)
		data = ser.data
		if data:
			fields = model_admin.list_display
		return render(request,'tables/table_detail.html',locals())
	
	def create(self, request, *args, **kwargs):
		model_form = creat_model_form(request,self.model_admin)
		obj = request.POST
		obj = model_form(obj)
		if obj.is_valid():
			obj.save()
			return redirect('table_data' ,self.app_name,self.table_name)
		return render(request, 'tables/table_add.html', locals())
	
	
	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		model_form=creat_model_form(request,self.model_admin)
		form_obj=model_form(instance=instance)
		return render(request,'tables/table_change.html',locals())
	
	def destroy(self, request, *args, **kwargs):
		instance = self.get_object()
		response={
			'status':1
		}
		if self.perform_destroy(instance):
			response['status']=0

		return HttpResponse(json.dumps(response))
		

