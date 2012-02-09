from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<obj_type>[\w\d\-]+)/(?P<obj>[\w\d\-]+)/(?P<action>[\w\d\-]+)/$', 
        'managers.log_mgr.views.log_ajax', name="logger_log_ajax"),
)
