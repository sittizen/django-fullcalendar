# -*- coding: utf-8 -*-
from django.db import models

from schedule.models import Event
from schedule.models.calendars import Calendar

COLOR_TYPE = ( #todo color codes blendig with bootstrap
    ('blue', '#1EB2DE'),
    ('red', '#EF4023'),
    ('yellow' , '#FFD52F'),
)
class FullCalendar(Calendar):
    color = models.CharField(max_length=6, choices=COLOR_TYPE)
    nb_slot = models.PositiveIntegerField()

class FullCalendarEvent(Event):
    pass
