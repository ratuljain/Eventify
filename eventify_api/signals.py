import StringIO
import os
import qrcode
from cloudinary.uploader import upload

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save, pre_init
from django.dispatch import receiver
from mock.mock import self
from rest_framework.authtoken.models import Token
import qrcode
from Eventify.settings import SERVICE_ACCOUNT_JSON_FILE
from eventify_api.models import Venue, Attachment, Event


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
        "serviceAccount": SERVICE_ACCOUNT_JSON_FILE
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


@receiver(post_save, sender=Event)
def save_qr_code_cloudinary(sender, instance, created, **kwargs):
    # if created:
    event = instance
    if not event.qr_code_url:
        img = qrcode.make(event.entry_code)
        filename = event.event_name.replace(" ", "_") + ".png"
        img.save("qrcode/" + filename)
        url = upload("qrcode/" + filename)['url']
        Event.objects.filter(id=instance.pk).update(qr_code_url=url)
        print url
