rapidsms-textit
============================

Basic `textit <http://www.textit.in>`_ backend for
`RapidSMS <http://www.rapidsms.org/>`_, version 0.14.0 or later.

Requirements
------------

 * `RapidSMS <http://www.rapidsms.org>`_, version 0.14.0 or later
    (pip install 'rapidsms>=0.14.0')
 * `Django <https://djangoproject.com>`_, version 1.4 or later.

Usage
-----

Create an application at textit.in.  Its type should be "Web API".

Add rtextit to your Python path and set up the textit backend in your Django
settings file.

The required settings for your textit backend in INSTALLED_BACKENDS are:

ENGINE
    "rtextit.outgoing.TextItBackend"

config
    A dictionary with the rest of your settings for this backend. Required
    settings inside `config` are:

    messaging_token
        Your messaging token from TextIt (a long hex string)

    number
        The phone number your TextIt app is using. Must start with "+" and the
        country code.

For example::

    INSTALLED_BACKENDS = {
        "my-textit-backend": {
            "ENGINE": "rtextit.outgoing.TextItBackend",
            'config': {
                # Your TextIt application's outbound token for messaging (required)
                'messaging_token': 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
                # Your TextIt application's voice/messaging phone number, starting
                # with "+" and the country code (required)
                'number': '+1-###-###-####',
            },
        },
    }

At this point you should be able to send outgoing messages, but more setup is needed to receiving incoming messages.

Set up your URLconf to send incoming http requests from textit to
`rtextit.views.message_received`, passing the backend_name parameter, whose
value must be the same as the backend name you used in INSTALLED_BACKENDS.

For example::

    from django.conf.urls.defaults import *
    from rtextit import views

    urlpatterns = patterns('',
        url(r"^textit/$",
            views.message_received,
            kwargs={'backend_name': 'my-textit-backend'},
            name='textit'),
    )

You can use any URL.  If you want to add some (slight) protection against
someone other than TextIt passing you messages pretending to be TextIt, you
might make your URL long and random, e.g.::

    from django.conf.urls.defaults import *
    from rtextit import views

    urlpatterns = patterns('',
        url(r"^534bd769-3e2e-42bd-8337-2099d9f38858/$",
            views.message_received,
            kwargs={'backend_name': 'my-textit-backend'},
            name='textit'),
    )

Configure your TextIt application at textit.in so its SMS/Messaging URL will invoke the Django URL that you just configured.  E.g.::

    https://yourserver.example.com/534bd769-3e2e-42bd-8337-2099d9f38858/

Background
----------

 * `TextIt's API doc <http://textit.in/api/v1>`_

Original from rapidsms-tropo by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.

Now called rapidsms_textit by `eHealth Africa <http://www.ehealthafrica.org/>`_.

Changelog
--------------------------------

Rapidsms-tropo v0.2.0 (Released 2013-05-20)
________________________________

