from django import forms
from django.contrib.auth.models import Group, User


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'permissions']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'groups', 'email', 'is_active']
