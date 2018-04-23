#__author:zhang_lei

class BaseKingAdmin(object):
  
    list_display=['id',]
    list_filters=[]
    search_fields=[]
    filter_condtions=[]
    filter_horizontal=[]
    readonly_fields=[]
    form_add=False
    list_per_page = 2
    ordering='id'
    def default_clean_form(self):
        pass
















