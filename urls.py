from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^tcpractice/$', 'topcoder.tcpractice.views.index'),
    (r'^tcpractice/create$', 'topcoder.tcpractice.views.create'),
    (r'^tcpractice/create_done$', 'topcoder.tcpractice.views.create_done'),
    (r'^tcpractice/login', 'topcoder.tcpractice.views.login'),
    # Example:
    # (r'^topcoder/', include('topcoder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
