# -*- coding: utf-8 -*-
from django.conf.urls import *

from .views import CalendarsView, EventSourceView, EventCreateView


urlpatterns = patterns('',

    url(r'^$', CalendarsView.as_view(), name='calendars'),

    url(r'^event-source/$', EventSourceView.as_view(), name='event-source'),
    url(r'^event-create/$', EventCreateView.as_view(), name='event-create'),

)
