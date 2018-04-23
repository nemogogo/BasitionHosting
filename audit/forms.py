#__author:zhang_lei
from django import forms
from django.forms import ModelForm,fields
from audit import models
from django.core.exceptions import ValidationError
class UserCreationForm(ModelForm):
    password1=forms.CharField(label='Password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model=models.UserProfile
        fields=['username','email']

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            from django.contrib.auth import models
            group = models.Group.objects.filter(name='staff')
            user.save()
            user.groups.add(*group)
        return user

    # def clean_password(self):
    #     if self.password=='abc12345':
    #         return self.password
    #     else:
    #         raise ValidationError("密码要是abc12345")