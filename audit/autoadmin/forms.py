from django.forms import forms,ModelForm
from django.utils.translation import ugettext as _
from django.forms import ValidationError
from audit import models

def creat_model_form(request,model_admin):

    class Meta:
        model=model_admin.model
        fields="__all__"
    def default_clean(self):
        error_list = []
        self.ValidationError = ValidationError
        if not hasattr(model_admin, "is_add_form"):
            print("-------------------default_clean")
            print('----------->>>>>',model_admin.readonly_fields)

            for field in model_admin.readonly_fields:
                field_val = getattr(self.instance, field)
                field_from_page = self.cleaned_data.get(field)
                if field in model_admin.filter_horizontal:
                    field_val = getattr(self.instance, field).select_related()
                    print(dir(field_val))
                    field_val=str(field_val.order_by('id'))
                    field_from_page=str(field_from_page.order_by('id'))
                print( (field_val), field_from_page)
                if field_val!= field_from_page:
                    error_list.append(ValidationError(
                        _("Field %(field)s is readonly,data should be %(val)s"),
                        code='invalid',
                        params={'field': field, 'val': field_val}
                    ))

        response=model_admin.default_clean_form()
        if response:
            error_list.append(response)
        if error_list:
            print(error_list)
            raise ValidationError(error_list)

    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
           
            if not hasattr(model_admin, "is_add_form"):  # 代表这是添加form,不需要disabled
                if field_name in model_admin.readonly_fields:
                    field_obj.widget.attrs['disabled'] = 'disabled'

       
            if hasattr(model_admin,"clean_%s"%field_name):
                clean_func=getattr(model_admin,"clean_%s"%field_name)
                setattr(cls,"clean_%s"%field_name,clean_func)

        return ModelForm.__new__(cls)

    _model_form_class=type("DynamicModelForm",(ModelForm,),{'Meta':Meta})

    setattr(_model_form_class, '__new__', __new__)
    setattr(_model_form_class, 'clean', default_clean)
    return _model_form_class