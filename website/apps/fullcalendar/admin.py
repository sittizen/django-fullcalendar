# -*- coding: utf-8 -*-
from django.contrib import admin
from schedule.models.calendars import Calendar
from schedule.models.events import  Event
from .models import FullCalendar, FullCalendarEvent

admin.site.unregister(Calendar)
admin.site.register(FullCalendar, admin.ModelAdmin)

admin.site.unregister(Event)
admin.site.register(FullCalendarEvent, admin.ModelAdmin)
