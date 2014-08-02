""" replace some rapidsms entry points for test purposes
"""
__author__ = 'vernon'

_CONNECTION_LIST = [42]

def lookup_connections(selector, from_address):
    return _CONNECTION_LIST

def receive(text, connection):
    assert connection == _CONNECTION_LIST[0]
    print('rapidsms_stub: Received Data="{}"'.format(text))
