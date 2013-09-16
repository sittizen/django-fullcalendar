# -*- coding: utf-8 -*-
from django.conf.urls import *

from .views import ( CalendarsView, EventSourceView, EventCreateView, CalendarListView, CalendarCreateView,
                     CalendarUpdateView, CalendarDeleteView, EventUpdateView, EventDeleteView )


urlpatterns = patterns('',

    url(r'^$', CalendarsView.as_view(), name='calendars'),

    url(r'^calendar-list/$', CalendarListView.as_view(), name='calendar-list'),
    url(r'^calendar-create/$', CalendarCreateView.as_view(), name='calendar-create'),
    url(r'^calendar-update/$', CalendarUpdateView.as_view(), name='calendar-update'),
    url(r'^calendar-delete/$', CalendarDeleteView.as_view(), name='calendar-delete'),

    url(r'^event-source/$', EventSourceView.as_view(), name='event-source'),
    url(r'^event-create/$', EventCreateView.as_view(), name='event-create'),
    url(r'^event-update/(?P<pk>\d+)/$', EventUpdateView.as_view(), name='event-update'),
    url(r'^event-delete/(?P<pk>\d+)/$', EventDeleteView.as_view(), name='event-delete'),

)
