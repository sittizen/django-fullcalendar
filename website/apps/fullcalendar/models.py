# -*- coding: utf-8 -*-
from django.db import models

from schedule.models import Event
from schedule.models.calendars import Calendar

COLOR_TYPE = ( #todo color codes blendig with bootstrap
    ('primary', '#285e8e'),
    ('success', '#398439'),
    ('info', '#269abc'),
    ('warning', '#d58512'),
    ('danger', '#ac2925'),

)
class FullCalendar(Calendar):
    color = models.CharField(max_length=7, choices=COLOR_TYPE)
    nb_slot = models.PositiveIntegerField()

class FullCalendarEvent(Event):
    pass
