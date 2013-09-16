from django.forms.util import flatatt, to_current_timezone
from django.forms.widgets import Select, DateInput, TextInput, MultiWidget

class JqSplitDateTimeWidget(MultiWidget):

    def __init__(self, attrs=None, date_format=None, time_format=None, time_widget='text'):
        date_class = attrs['date_class']
        time_class = attrs['time_class']
        del attrs['date_class']
        del attrs['time_class']

        time_attrs = attrs.copy()
        time_attrs['class'] = time_class
        date_attrs = attrs.copy()
        date_attrs['class'] = date_class

        if time_widget == 'text':
            hour_widget = TextInput(attrs=time_attrs)
            minute_widget = TextInput(attrs=time_attrs)
        else:
            hour_choices = ((0, '00'), (1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'),
                            (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'), (11, '11'),
                            (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'),
                            (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, 23),)
            minute_choices = ((0, '00'), (10, '10'), (20, '20'), (30, '30'), (40, '40'), (50, '50'), )
            hour_widget = Select(choices=hour_choices, attrs=time_attrs)
            minute_widget = Select(choices=minute_choices, attrs=time_attrs)

        widgets = (DateInput(attrs=date_attrs, format=date_format),
                   hour_widget, minute_widget,)

        super(JqSplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            d = value.date()
            hour = value.time().hour
            minute = value.time().minute
            return (d, hour, minute,)
        else:
            return (None, None, None, None)

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), it inserts an HTML
        linebreak between them.

        Returns a Unicode string representing the HTML for the whole lot.
        """
        return "%s %s:%s" % (rendered_widgets[0], rendered_widgets[1], rendered_widgets[2])
