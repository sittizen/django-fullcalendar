# -*- coding: utf-8 -*-
from django import forms

from .models import FullCalendar, FullCalendarEvent


class FullCalendarEventForm(forms.ModelForm):
    #end_recurring_period = forms.DateTimeField(widget=forms.SplitDateTimeWidget, required=False)
    calendar = forms.ModelChoiceField(queryset=FullCalendar.objects.all(), empty_label=None, required=True)
    date_start = forms.DateField()
    time_start = forms.TimeField()
    date_end = forms.DateField()
    time_end = forms.TimeField()

    class Meta:
        model = FullCalendarEvent
        fields = ('calendar', 'date_start', 'time_start', 'date_end', 'time_end', 'title', 'description', 'start', 'end', )

        exclude = ('creator', 'created_on', 'end_recurring_period', 'rule', )
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'text'}),
            'description' : forms.Textarea(attrs={'class' : 'desc', 'cols' : 48, 'rows' : 4}),
            'start': forms.TextInput(attrs={'style' : 'display:none;'}),
            'end': forms.TextInput(attrs={'style' : 'display:none;'})
        }

