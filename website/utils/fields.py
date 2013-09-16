import datetime
from time import strptime, strftime
from django import forms
from django.forms import fields
from django.forms.util import  from_current_timezone
from .widgets import JqSplitDateTimeWidget

class JqSplitDateTimeField(fields.MultiValueField):
    widget = JqSplitDateTimeWidget

    def __init__(self, *args, **kwargs):
        """
        Have to pass a list of field types to the constructor, else we
        won't get any data to our compress method.
        """
        all_fields = (
            fields.CharField(max_length=10),
            fields.IntegerField(),
            fields.IntegerField(),
        )
        super(JqSplitDateTimeField, self).__init__(all_fields, *args, **kwargs)

    def compress(self, data_list):
        """
        Takes the values from the MultiWidget and passes them as a
        list to this function. This function needs to compress the
        list into a single object to save.
        """
        if data_list:
            if not data_list[0] or data_list[1] in (None, '') or data_list[2] in (None, ''):
                raise forms.ValidationError("Field is missing data.")

            datetime_string = "%s %s:%s" % (data_list[0], data_list[1], data_list[2])
            datetime_obj = datetime.datetime.strptime(datetime_string, "%d/%m/%Y %H:%M")
            return datetime_obj
        return None
