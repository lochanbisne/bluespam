from django.conf.urls.defaults import *

from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', 'spam.site.views.status'),
                       (r'^stats/$', 'spam.site.views.stats'),
                       (r'^clear_sent/$', 'spam.site.views.clear_sent'),
                       (r'^clear_blacklist/$', 'spam.site.views.clear_blacklist'),
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.MEDIA_ROOT}),
                       (r'^admin/(.*)', admin.site.root),
                       )
