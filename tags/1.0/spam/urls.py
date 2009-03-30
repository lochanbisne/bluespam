from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^$', 'spam.site.views.status'),
                       (r'^status/$', 'spam.site.views.status'),
                       (r'^clear_sent/$', 'spam.site.views.clear_sent'),
                       (r'^clear_blacklist/$', 'spam.site.views.clear_blacklist'),
                       (r'^admin/(.*)', admin.site.root),
                       )
