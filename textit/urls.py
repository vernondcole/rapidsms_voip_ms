from django.conf.urls import patterns, url

from . import views
from .tests import live_receive_test

urlpatterns = patterns('',  # nopep8
    url(r'^$', views.index, name='index'),
    url(r"^test_textit/$", views.message_received, {'backend_name': 'test-textit-backend'}, name='textit',),
    url(r"^(?P<rcvd_url>)/$", live_receive_test.message_echo)
)
