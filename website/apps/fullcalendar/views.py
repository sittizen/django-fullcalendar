# -*- coding: utf-8 -*-
from apps.fullcalendar.models import FullCalendarEvent
from braces.views import CsrfExemptMixin, AjaxResponseMixin, JSONResponseMixin
from datetime import datetime, timedelta

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_spaces_between_tags as short
from django.views.generic import ListView, View, CreateView, FormView, UpdateView, DeleteView

from schedule.periods import Month
from schedule.utils import coerce_date_dict
from schedule.views import calendar_by_periods, get_occurrence
from schedule.conf.settings import GET_EVENTS_FUNC, OCCURRENCE_CANCEL_REDIRECT

from .models import FullCalendar
from .forms import FullCalendarEventForm

occtimeformat = 'ST%Y%m%d%H%M%S'

def _encode_occurrence(occ):
    """
        Create a temp id containing event id, encoded id if it is persisted,
        otherwise timestamp.
        Used by AJAX implementations so that JS can assemble a URL
        for calls to occurrence_edit
    """
    if occ.id:
        s = 'ID%d' % occ.id
    else:
        s = occ.start.strftime(occtimeformat)
    return 'E%d_%s' % (occ.event.id, s)


def _decode_occurrence(id):
    """
        reverse of encode_occurrence - given an encoded string
        returns a dict containing event_id and occurrence data
        occurrence data contain either occurrence_id
        or year, month etc.
    """
    try:
        res = {}
        parts = id.split('_')
        res['event_id'] = parts[0][1:]
        occ = parts[1]
        if occ.startswith('ID'):
            res['occurrence_id'] = occ[2:]
        else:
            start = datetime.datetime.strptime(occ, occtimeformat)
            occ_data = dict(year=start.year, month=start.month, day=start.day,
                            hour=start.hour, minute=start.minute, second=start.second)
            res.update(occ_data)
        return res
    except IndexError:
        return

class CalendarsView(ListView):
    context_object_name = 'calendars'
    model = FullCalendar
    template_name = 'fullcalendar/calendars.html'

    def get_context_data(self, **kwargs):
        ctx = super(CalendarsView, self).get_context_data(**kwargs)

        date = coerce_date_dict(self.request.GET)
        if date:
            try:
                date = datetime.datetime(**date)
            except ValueError:
                raise Http404
        else:
            date = timezone.now()

        ctx.update({
            'now' : datetime.now(),
            'date' : date,
        })

        return ctx

class CalendarListView(CsrfExemptMixin, ListView):
    context_object_name = 'calendars'
    model = FullCalendar
    template_name = 'fullcalendar/calendar_list.html'

class CalendarCreateView(CsrfExemptMixin, CreateView):
    context_object_name = 'calendar'
    model = FullCalendar
    template_name = 'fullcalendar/calendar_detail.html'

class CalendarUpdateView(CsrfExemptMixin, UpdateView):
    context_object_name = 'calendar'
    model = FullCalendar
    template_name = 'fullcalendar/calendar_detail.html'

class CalendarDeleteView(CsrfExemptMixin, DeleteView):
    context_object_name = 'calendar'
    model = FullCalendar
    template_name = 'fullcalendar/calendar_detail.html'


class EventSourceView(CsrfExemptMixin, AjaxResponseMixin, JSONResponseMixin, View):
    def post_ajax(self, request, *args, **kwargs):
        try:
            event_list = []
            for event in FullCalendarEvent.objects.filter(calendar__slug=request.POST['calendar_slug']):
                start = datetime.fromtimestamp(float(request.POST['start']), tz=timezone.get_default_timezone())
                end = datetime.fromtimestamp(float(request.POST['end']), tz=timezone.get_default_timezone())
                for occurence in  event.get_occurrences(start, end):
                    event_list.append({
                        'id': _encode_occurrence(occurence),
                        'event_id': event.pk,
                        'title': occurence.title,
                        'start': occurence.start.isoformat(),
                        'end': occurence.end.isoformat(),
                        'recurring': bool(occurence.event.rule),
                        'persisted': bool(occurence.id),
                        'description': occurence.description.replace('\n', '\\n'),
                        'allDay': False,
                        'cancelled': occurence.cancelled,
                    })
        except Exception, e:
            print str(e)
            raise
        finally:
            return self.render_json_response(event_list)

class EventCreateView(CsrfExemptMixin, CreateView):
    context_object_name = 'event'
    form_class = FullCalendarEventForm
    model = FullCalendarEvent
    template_name = 'fullcalendar/event_detail.html'
    success_url = reverse_lazy('fullcalendar:calendars')

    def get_initial(self):
        initial = self.initial.copy()
        if self.request.method == 'GET':
            if self.request.GET.has_key('calendar'):
                initial['calendar'] = self.request.GET['calendar']
            tz = timezone.get_default_timezone()
            initial['start'] = datetime.fromtimestamp(int(self.request.GET['start']), tz=tz)
            initial['end'] = datetime.fromtimestamp(int(self.request.GET['end']), tz=tz)
        return initial

class EventUpdateView(CsrfExemptMixin, UpdateView):
    context_object_name = 'event'
    form_class = FullCalendarEventForm
    model = FullCalendarEvent
    template_name = 'fullcalendar/event_detail.html'
    success_url = reverse_lazy('fullcalendar:calendars')

    def get_object(self, queryset=None):
        obj = super(EventUpdateView, self).get_object(queryset)
        if self.request.method == 'GET':
            day_delta = int(self.request.GET.get('day_delta', 0))
            if self.request.GET.get('action_type', 'clicked') == 'dragged':
                obj.start = obj.start + timedelta(days=day_delta)
            obj.end = obj.end + timedelta(days=day_delta)
        return obj

class EventDeleteView(CsrfExemptMixin, DeleteView):
    context_object_name = 'event'
    model = FullCalendarEvent
    template_name = 'fullcalendar/event_delete.html'
    success_url = reverse_lazy('fullcalendar:calendars')
