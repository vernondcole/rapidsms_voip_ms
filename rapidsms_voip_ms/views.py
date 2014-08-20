# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from __future__ import print_function, unicode_literals

import logging

from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


logger = logging.getLogger('textit.views')

if 'rapidsms' in settings.INSTALLED_APPS:
    from rapidsms.router import receive, lookup_connections
else:
    print('NOTE: loading test stub for RapidSMS.')
    from tests.rapidsms_stub import receive, lookup_connections

@csrf_exempt
@require_GET
def message_received(request, backend_name):
    """Handle HTTP requests from voip.ms.
SMS URL Callback: By enabling this option you will be able to send the messages to another destination e.g. your own server. If selected SMS Messages received by your DID will Send a GET request to the URL Callback provided. Available Variables for your URL:
 {FROM} The phone number that sent you the message
 {TO} The DID Number that receive the message
 {MESSAGE} The content of the message
 Example: http: //mysite.com/sms.php?to={TO}&from={FROM}&message={Message}

    """
    try:
        backend = settings.INSTALLED_BACKENDS[backend_name]
    except KeyError:
        logger.error('Name "{}" not found in settings INSTALLED_BACKENDS.'.format(backend_name))
        return HttpResponseBadRequest('Name "{}" not found in settings INSTALLED_BACKENDS.'.format(backend_name))
    try:
        if request.META['QUERY_STRING'] != backend['config']['query_key']:
            r = 'query_key "{}" does not match configured value from django settings "{}"'.format(
                    request.META['QUERY_STRING'], backend['config']['query_key'])
            logger.error(r)
            return HttpResponseBadRequest(r)
    except KeyError:
        logger.error("No query_key set up in settings INSTALLED_BACKENDS[backend_name]")
        return  HttpResponseBadRequest("No query_key set up in settings INSTALLED_BACKENDS[backend_name]")

    post = request.POST
    logger.debug("@@ request from TextIt - Decoded data: %r" % post)
    try:
        post_event = post['event']
    except KeyError:
        logger.error('No "Event" key in POST request')
        return HttpResponseBadRequest("No Event key in POST request")
    if post_event == 'mo_sms':
        # Must have received a message
        logger.debug("@@Got a text message")
        try:
            fa = post['phone']
            from_address = fa[1:] if fa.startswith('+') else fa  # strip off the plus sign
            text = post['text']
            logger.debug("@@Received message from %s: %s" % (from_address, text))
        except KeyError:
            logger.exception('Malformed POST message')
            return HttpResponseBadRequest("Malformed POST message")
        try:
            # pass the message to RapidSMS
            connections = lookup_connections(backend_name, [from_address])
            receive(text, connections[0])
        except Exception:
            r = "Error finding connection for backend_name={}, from={}".format(
                backend_name, from_address)
            logger.error(r)
            return HttpResponseServerError(r)
        # Respond nicely to TextIt
        return HttpResponse("OK")

    # else:
    logger.error("@@No recognized command in request from TextIt")
    return HttpResponseBadRequest("Unexpected event code='{}'".format(post_event))

def index(request):
    return HttpResponse("Hello, world. You're at the TextIt_test index.")
