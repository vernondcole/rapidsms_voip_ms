rapidsms-textit
============================

Basic `voip.ms <http://www.voip.ms>`_ backend for
`RapidSMS <http://www.rapidsms.org/>`_, version 0.14.0 or later.

Requirements
------------

 * `RapidSMS <http://www.rapidsms.org>`_, version 0.14.0 or later
    (pip install rapidsms)
 * `Django <https://djangoproject.com>`_,
    (pip install django)
 *  (for testing):  `pip install mock`

Usage
-----

Create an application at textit.in.  Its type should be "Web API".

Add rapidsms_textit to your Python path and set up the textit backend in your Django
settings file.

The required settings for your textit backend in INSTALLED_BACKENDS are:

ENGINE
    "rapidsms_textit.outgoing.TextItBackend"

config
    A dictionary with the rest of your settings for this backend. Required
    settings inside `config` are:

    messaging_token
        Your messaging token from TextIt (a long hex string)

    number
        The phone number your TextIt app is using. Must start with "+" and the
        country code.

    query_key
        A low-grade authorization key to help guard against the most simple attempts
        to sneak false information in to the system. It will be expected to be sent
        (as clear text) as a query string in the URL of POST requests from text.it

For example::

    INSTALLED_BACKENDS = {
        "my-textit-backend": {
            "ENGINE": "rapidsms_textit.outgoing.TextItBackend",
            'config': {
                # Your TextIt application's outbound token for messaging (required)
                'api_token': 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY',
                # Your TextIt application's messaging phone number, starting
                # with "+" and the country code (required)
                'number': '+1##########',
                # and the string you will have text.it send at the end of your URL like:
                # http://your.site.org/textit/my/?key=MumbleMumble
                'query_key': 'key=MumbleMumble'
                # optionally, you may define a different URL address for the textit server. The default is:
                # 'api_url': 'https://api.textit.in/api/v1/'
            },
        },
    }

At this point you should be able to send outgoing messages, but more setup is needed to receiving incoming messages.

Set up your URLconf to send incoming http requests from textit to
`rapidsms_textit.views.message_received`, passing the backend_name parameter, whose
value must be the same as the backend name you used in INSTALLED_BACKENDS.

For example::

    from django.conf.urls.defaults import *
    from rapidsms_textit import views

    urlpatterns = patterns('',
        url(r"^textit/my/$",
            views.message_received,
            kwargs={'backend_name': 'my-textit-backend'},
            name='textit'),
    )


You can test your implementation by sending a POST request using "curl" something like:
`$curl -X POST localhost:8000/textit/x/?key=MumbleMumble -d "status=P&direction=I&relayer=2166&text=Twenty+four&sms=443263&phone=%2B2348092545605&time=2014-07-31T13%3A58%3A15.000000&relayer_phone=%2B23480998904&event=mo_sms"`


Background
----------

 * `TextIt's API doc <http://textit.in/api/v1>`_

Heavily borrowed from rapidsms-tropo by `Caktus Consulting Group <http://www.caktusgroup.com/>`_.

Now rapidsms_textit by `eHealth Africa <http://www.ehealthafrica.org/>`_.

Changelog
--------------------------------

Rapidsms-tropo v0.2.0 (Released 2013-05-20)
________________________________

