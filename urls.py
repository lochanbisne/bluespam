from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'spam.site.views.status'),
                       (r'^status/$', 'spam.site.views.status'),
                       (r'^clear_sent/$', 'spam.site.views.clear_sent'),
                       (r'^clear_blacklist/$', 'spam.site.views.clear_blacklist'),

# Uncomment this for admin:
(r'^admin/', include('django.contrib.admin.urls')),
)
