from __future__ import unicode_literals

from django.apps import AppConfig


class EventifyApiConfig(AppConfig):
    name = 'eventify_api'

    def ready(self):
        from eventify_api import signals
