# -*- coding: utf-8 -*-
# Useful Links:
# http://ccbv.co.uk/
# http://django-braces.readthedocs.org/en/latest/index.html
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, RedirectView


class HomepageView(RedirectView):
    url = reverse_lazy('fullcalendar:calendar-by-periods')
