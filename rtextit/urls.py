from django.conf.urls import patterns, url

from . import views
from .tests import live_receive_test

urlpatterns = patterns('',  # nopep8
    url(r'^$', views.index, name='index'),
    url(r"^textit/webhook/$", views.message_received, name='textit'),
    url(r"^(?P<rcvd_url>[\w-]+)/$", live_receive_test.message_echo)
)
