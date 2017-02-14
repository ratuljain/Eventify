import os

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_init
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from eventify_api.models import Venue, Attachment


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Attachment)
def do_something(sender, instance, created, **kwargs):
    import pyrebase

    config = {
        "apiKey": "AIzaSyBOvqjUrM1juX2ZiPD1HwDQOjvKPY0q9nM",
        "authDomain": "eventifyapp-d5196.firebaseapp.com",
        "databaseURL": "https://eventifyapp-d5196.firebaseio.com/",
        "storageBucket": "eventifyapp-d5196.appspot.com",
        "serviceAccount": "/Users/ratuljain/PycharmProjects/Eventify/eventify_api/serviceAccountCredentials.json"
    }

    # get name of file
    filename = os.path.basename(instance.file.url)
    firebase = pyrebase.initialize_app(config)
    storage = firebase.storage()
    storage.child(filename).put(instance.file.url)
    upload_link = storage.child(filename).get_url(None)

    if created:
        instance.attachment_url = upload_link
        instance.file_name = filename
        instance.save()

# post_save.connect(do_something, sender=Venue)
