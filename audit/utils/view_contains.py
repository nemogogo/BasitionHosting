from django.db.models import Q

def table_filter(request,model_admin):
     '''进行条件过滤并返回过滤后的数据'''
     filter_conditions={}
     keywords=['page','o','_q']
     for k,v in request.GET.items():
         if k in keywords:
             '''保留的分页关键字，and 排序关键字'''
             continue
         if v:
             filter_conditions[k]=v
     # print('---->filter_conditions',filter_conditions)
     return model_admin.model.objects.filter(**filter_conditions).order_by("%s" % model_admin.ordering if model_admin.ordering else  "id"),filter_conditions
def table_search(request,admin_class,obj_list):
    search_key=request.GET.get('_q','')
    q_obj=Q()
    q_obj.connector='OR'
    for column in admin_class.search_fields:
        q_obj.children.append(('%s__contains'%column,search_key))

    res=obj_list.filter(q_obj)
    return res

 