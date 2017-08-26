from django import forms
from django.contrib.auth.models import Group, User


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'
