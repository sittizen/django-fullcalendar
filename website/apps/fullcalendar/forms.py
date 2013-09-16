# -*- coding: utf-8 -*-
from django import forms

from .models import FullCalendar, FullCalendarEvent
from website.utils.fields import JqSplitDateTimeField
from website.utils.widgets import JqSplitDateTimeWidget


class FullCalendarEventForm(forms.ModelForm):
    #end_recurring_period = forms.DateTimeField(widget=forms.SplitDateTimeWidget, required=False)
    calendar = forms.ModelChoiceField(queryset=FullCalendar.objects.all(), empty_label=None, required=True)
    start = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(date_format='%d/%m/%Y', attrs={'maxlength':2, 'date_class':'datepicker','time_class':'timepicker'}))
    end = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(date_format='%d/%m/%Y', attrs={'maxlength':2, 'date_class':'datepicker','time_class':'timepicker'}))

    class Meta:
        model = FullCalendarEvent
        fields = ('calendar', 'title', 'description', 'start', 'end', )

        exclude = ('creator', 'created_on', 'end_recurring_period', 'rule', )
        widgets = {
            'title': forms.TextInput(attrs={'class' : 'text'}),
            'description' : forms.Textarea(attrs={'class' : 'desc', 'cols' : 48, 'rows' : 4}),
        }

