#!/usr/bin/python
"""Send a general SMS message from the command line."""
from __future__ import print_function, unicode_literals
__author__ = 'vernon'

import datetime

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from rapidsms_textit.outgoing import TextItBackend


class Command(BaseCommand):
    help = 'textit_txt [phone, phone ...] put your outgoing message here.'

    def handle(self, *args, **options):
        self.txt(*args)

    def txt(self,*args):

        if len(args) < 2:
            print(help)

        numbertoken = args[0].replace('-','')
        if numbertoken.startswith('[') and numbertoken.endswith(']'):
            numbers = [nmbr.strip() for nmbr in numbertoken[1:-1].split(',')]
        else:
            numbers = [numbertoken]

        for number in numbers:
            if len(number) < 8 or not number.startswith('+') or not number[1:].isnumeric():
                raise CommandError('Numbers must have "+countrycode" form. "{}" is wrong'.format(number))

        T = TextItBackend(NotImplemented, 'textit', config=settings.INSTALLED_BACKENDS['test-textit-backend']['config'])
        T.send(NotImplemented, ' '.join(args[1:]), numbers, NotImplemented)

        print('Sent "{}" to {!r}'.format(' '.join(args[1:]), numbers))
