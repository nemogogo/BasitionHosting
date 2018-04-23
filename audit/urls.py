#__author:zhang_lei
from django.conf.urls import url
from audit import views
from audit.views import TableView
urlpatterns=[
    url(r'^login/$',views.acc_login,name='login'),
    url(r'^logout/$',views.acc_logout,name='logout'),
    url(r'^register/$',views.register,name='register'),
    url(r'^index/$', views.index, name='index'),
    url(r'^web-ssh/$', views.web_ssh,name='web-ssh'),
	url(r'^batch-task/$', views.batch_task, name='batch_task'),
	url(r'^file_transfer/$', views.file_transfer, name='file_transfer'),
	url('^batch_task_manager/$', views.batch_task_manager, name='batch_task_manager'),
	url(r'^task_result/$', views.task_result, name='get_task_result'),
   
   
]