# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from __future__ import print_function, unicode_literals
import json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def message_echo(request, rcvd_url):
    """Handle HTTP requests from TextIt.
    """

    #
    # if 'program' in parms:
    #     # Execute a program that we passed to TextIt to pass back to us.
    #     # Extract the program, while verifying it came from us and
    #     # has not been modified.
    #     try:
    #         program = signing.loads(parms['program'])
    #     except signing.BadSignature:
    #         logger.exception("@@ received program with bad signature")
    #         return HttpResponseBadRequest()
    print('rcvd_url="{}"'.format(rcvd_url))
    print('path={}'.format(request.get_full_path()))
    if request.method != 'POST':
        print('Unexpected method={}'.format(request.method))
        return HttpResponseNotAllowed(['POST'])
    print('POST={!r}'.format(request))
    if request.POST['text'].starts_with('echo '):
        js = {'phone': request.POST['phone'],
              'text': 'Okay<{}>'.format(request.POST['text'])
        }
        return HttpResponse(json.dumps(js))
    # else:
    return HttpResponse("Ok")
