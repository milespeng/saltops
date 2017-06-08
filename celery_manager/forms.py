from djcelery.models import IntervalSchedule
from django import forms


class IntervalScheduleForm(forms.ModelForm):
    class Meta:
        model = IntervalSchedule
        fields = ['every', 'period']
