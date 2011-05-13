from django.conf.urls.defaults import *


urlpatterns = patterns('verify_email.tests.views',
    url('^simple-view/$', 'simple_view'),
    url('^other-view/$', 'other_view'),
    url('^other-view2/$', 'other_view2'),
)
