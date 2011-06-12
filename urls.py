from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^tcpractice/$', 'topcoder.tcpractice.views.index'),
    (r'^tcpractice/create$', 'topcoder.tcpractice.views.create'),
    (r'^tcpractice/create_done$', 'topcoder.tcpractice.views.create_done'),
    (r'^tcpractice/detail', 'topcoder.tcpractice.views.detail'),
    (r'^tcpractice/login', 'topcoder.tcpractice.views.login_view'),
    (r'^tcpractice/logout$', 'topcoder.tcpractice.views.logout_view'),
    (r'^tcpractice/create_user$', 'topcoder.tcpractice.views.create_new_user'),
    # Example:
    # (r'^topcoder/', include('topcoder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
