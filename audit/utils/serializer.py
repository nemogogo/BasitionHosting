#__author:zhang_lei
from audit.autoadmin.sites import site
from audit import models
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer,Serializer,HyperlinkedModelSerializer
def check_table_permission(func):
    def inner(*args):
        if not args[0].user.is_superuser:
            pass
        return func(*args)
    return inner
def create_serializer(model,fields,**kwargs):
	
    attrs={}
    print('serializing---------')
    for field in fields:
	    field_name=field
	    field = serializers.CharField()
	    if model._meta.get_field(field_name).get_internal_type() == 'SmallIntegerField':
		    if model._meta.get_field(field_name).flatchoices:
			    field=serializers.CharField(source='get_%s_display'%field_name)
	    
	    if model._meta.get_field(field_name).get_internal_type() == 'ManyToManyField':
		    field = serializers.CharField(source='%s.all.values' % field_name)
	 
	    if len(fields) == 1:
		    field = serializers.CharField()
		
	    attrs[field_name]=field
		
    name = 'DynamicModelSerializer'
    
    baseclasess = (Serializer,)
   
    model_serializer = type(name, baseclasess,attrs)
   
    if kwargs.get("request"): #for form validator
        setattr(model_serializer,'_request',kwargs.get("request"))
	   
    return model_serializer

