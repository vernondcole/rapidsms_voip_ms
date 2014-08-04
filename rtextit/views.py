# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from __future__ import print_function, unicode_literals

import logging

from django.http import HttpResponse, HttpResponseServerError, HttpResponseBadRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


logger = logging.getLogger('rtextit.views')

if 'rapidsms' in settings.INSTALLED_APPS:
    from rapidsms.router import receive, lookup_connections
else:
    print('NOTE: loading test stub for RapidSMS.')
    from tests.rapidsms_stub import receive, lookup_connections

@csrf_exempt
@require_POST
def message_received(request, backend_name):
    """Handle HTTP requests from TextIt.
    """
    try:
        if request.META['QUERY_STRING'] != settings.INSTALLED_BACKENDS['textit-backend']['config']['query_key']:
            return HttpResponseBadRequest(
                'query_key "{}" does not match configured value from django settings "{}"'.format(
                    request.META['QUERY_STRING'], settings.INSTALLED_BACKENDS['textit-backend']['config']['query_key']))
    except Exception:
        raise
        return  HttpResponseBadRequest("No query_key set up in settings INSTALLED_BACKENDS['textit_backend']")

    post = request.POST
    logger.debug("@@ request from TextIt - Decoded data: %r" % post)
    print('views.message_received: post=',repr(post)) ###
    post_event = post['event']
    if post_event == 'mo_sms':
        # Must have received a message
        logger.debug("@@Got a text message")
        try:
            from_address = post['phone']
            text = post['text']
            logger.debug("@@Received message from %s: %s" % (from_address, text))

            # pass the message to RapidSMS
            connections = lookup_connections(backend_name, from_address)
            receive(text, connections[0])

        except Exception:
            logger.exception("@@responding to textit with error")
            return HttpResponseServerError("Error finding connection for backend_name={}, from={}".format(
                backend_name, from_address))
        # Respond nicely to TextIt
        return HttpResponse("OK")
    # elif:
    if post_event in ['mt_sent', 'mt_dlvd']:
        return HttpResponse("thanks")  # confirmation messages are ignored
    # else:
    logger.error("@@No recognized command in request from TextIt")
    return HttpResponseBadRequest("Unexpected event code='{}'".format(post_event))

def index(request):
    return HttpResponse("Hello, world. You're at the rTextIt_test index.")
