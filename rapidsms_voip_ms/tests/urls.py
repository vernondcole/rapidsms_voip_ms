from django.conf.urls import patterns, url

from ..views import message_received

urlpatterns = patterns('',  # nopep8
    url(r"^backend_textit/$", name="textit-backend",
        view=message_received,
        kwargs={'backend_name': 'my-backend'}),

    # Dummies
    url(r"^rapidsms-login", name="rapidsms-login", view=message_received),
)
