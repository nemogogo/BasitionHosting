from django.template import Library

from django.utils.safestring import mark_safe
import datetime
from datetime import timedelta
register=Library()

@register.simple_tag
def parse_response(response):
	print(dir(response))
	print(response.data['detail'])
 
	print(type(response))
	return response


@register.simple_tag
def get_field_value(obj,field):
 
	return getattr(obj,field)

@register.simple_tag
def build_pagination(pg):
	pgstr=""
	page_list=[x for x in  range(pg.page.number-3,pg.page.number+3) if x >0 and x<=pg.page.paginator.num_pages]
	for page_num in page_list:
		pg_li="<li><a href='?page=%s'>%s</a></li>"%(page_num,page_num)
		if page_num==pg.page.number:
			pg_li = "<li  class='active'><a href='?page=%s'>%s</a></li>" % (page_num, page_num)
		pgstr+=pg_li
		
 
	return mark_safe(pgstr)

@register.simple_tag
def build_filter_field(field,model_name,filter_condtions):
	select_ele = '''<select class="form-control " name='{field}' id={field}><option value=''>-----</option>'''
	field_obj = model_name.model._meta.get_field(field)
	if field_obj.get_internal_type() =='BooleanField':
		selected = ''
		for choice_item in ['True','False']:
			if filter_condtions.get(field) == str(choice_item[0]):
				selected = "selected"
			select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item, selected, choice_item)
			selected = ''
	if field_obj.choices:
		selected = ''
		for choice_item in field_obj.choices:
			if filter_condtions.get(field) == str(choice_item[0]):
				selected = "selected"
			select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
			selected = ''
	if type(field_obj).__name__ == "ForeignKey":
		selected = ''
		for choice_item in field_obj.get_choices()[1:]:
			if filter_condtions.get(field) == str(choice_item[0]):
				selected = "selected"
			select_ele += '''<option value='%s' %s>%s</option>''' % (choice_item[0], selected, choice_item[1])
			selected = ''
	# print('---->foreignkey',select_ele)
	if type(field_obj).__name__ in ['DateTimeField', 'DateField']:
		date_els = []
		today_ele = datetime.now().date()
		date_els.append(['今天', datetime.now().date()])
		date_els.append(["昨天", today_ele - timedelta(days=1)])
		date_els.append(["近7天", today_ele - timedelta(days=7)])
		date_els.append(["本月", today_ele.replace(day=1)])
		date_els.append(["近30天", today_ele - timedelta(days=30)])
		date_els.append(["近90天", today_ele - timedelta(days=90)])
		date_els.append(["近180天", today_ele - timedelta(days=180)])
		date_els.append(["本年", today_ele.replace(month=1, day=1)])
		date_els.append(["近一年", today_ele - timedelta(days=365)])
		
		selected = ''
		for item in date_els:
			select_ele += '''<option value='%s' %s>%s</option>''' % (item[1], selected, item[0])
		
		filter_field_name = "%s__gte" % field
		
		
	else:
		filter_field_name = field
		
	# print('tags---->2', filter_field_name)
	select_ele += "</select>"
	select_ele = select_ele.format(field=filter_field_name,select_name=field_obj.verbose_name.upper())
	
	return mark_safe(select_ele)
	
	
	
	