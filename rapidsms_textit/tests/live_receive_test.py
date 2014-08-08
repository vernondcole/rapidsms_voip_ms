# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from __future__ import print_function, unicode_literals
import json

from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def message_echo(request, rcvd_url):
    """Handle HTTP requests from TextIt.
    """
    print('live_receive_test: rcvd_url="{}"'.format(rcvd_url))
    if request.method != 'POST':
        print('  Unexpected method={}'.format(request.method))
        return HttpResponseNotAllowed(['POST'])
    # else:
    for key in request.POST:
        print('  {}="{}"'.format(key, request.POST[key]))
    if request.POST['text'].startswith('echo '):
        print('  Echoing:"{}"'.format(request.POST['text'][5:]))
        js = {'phone': request.POST['phone'],
              'relayer': request.POST['relayer'],
              'text': 'Okay<{}>'.format(request.POST['text'][5:])
        }
        return HttpResponse(json.dumps(js), content_type='application/json', status=200)
    # else:
    return HttpResponse("Ok", status=200)
