from django.conf import settings
from django.conf.urls import url, patterns, include

from django.contrib import admin
from .views import HomepageView

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^$', HomepageView.as_view(), name='homepage'),

    url(r'^inplaceeditform/', include('inplaceeditform.urls')),

    url(r'^fullcalendar/', include('apps.fullcalendar.urls', namespace='fullcalendar', app_name='fullcalendar')),
)

if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
