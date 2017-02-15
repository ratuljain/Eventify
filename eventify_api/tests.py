import os
import pyrebase
import requests
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from unittest2 import TestCase

from eventify_api.utils import parse_firebase_token
from models import Venue, Attachment


class VenueTests(APITestCase):

    def setUp(self):
        venue = Venue(venue_name="TestVenue", venue_seat_capacity=50)
        venue.save()

    def test_list_venues(self):
        """
        Ensure we can retrieve list of venues.
        """
        url = reverse('venue-list')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail_venues(self):
        """
        Ensure we can retrieve a venue by pk.
        """
        url = reverse('venue-detail', kwargs={'pk': 1})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        pass


class EventifyUserTokenGenerationTests(TestCase):

    def test_token_creation_on_new_user(self):
        """
        Ensure we can retrieve list of venues.
        """
        # print self.created_auth_user
        u = User(username='ghjcsdbjhcw')
        u.save()
        self.assertIsNotNone(Token.objects.get(user=u))


class EventifyAttachmentCreationTest(TestCase):
    attachment = None

    def setUp(self):
        self.attachment = Attachment(
            file="/Users/ratuljain/PycharmProjects/Eventify/documents/eventify_model.pdf")
        self.attachment.save()

    def test_attachment_url_creation(self):
        """
        Ensure we can retrieve list of venues.
        """
        # check if URL actually exists
        attach_url = self.attachment.attachment_url
        request = requests.get(attach_url)
        self.assertEqual(request.status_code, status.HTTP_200_OK)


class FirebaseJWParsingTest(TestCase):
    firebase_user = None
    login_mail = "testuser@test.com"

    def setUp(self):

        dir_path = os.path.dirname(os.path.abspath(__file__))
        serviceAccount_file_path = os.path.join(dir_path, "serviceAccountCredentials.json")

        config = {
            "apiKey": "AIzaSyBOvqjUrM1juX2ZiPD1HwDQOjvKPY0q9nM",
            "authDomain": "eventifyapp-d5196.firebaseapp.com",
            "databaseURL": "https://eventifyapp-d5196.firebaseio.com/",
            "storageBucket": "eventifyapp-d5196.appspot.com",
            "serviceAccount": serviceAccount_file_path
        }

        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password(
            self.login_mail, 'password')
        self.firebase_user = user

    def test_firebase_token_parsing(self):
        """
        Ensure we can retrieve user details after parsing firebase jwt token that we get after a successful log in.
        """
        # check if URL actually exists
        id_token = self.firebase_user['idToken']
        user_email = parse_firebase_token(id_token)['email']
        self.assertEqual(user_email, self.login_mail)

    def test_check_if_signals_work(self):
        """
        Ensure if signals are being called. Make sure to import signals.py in EventifyApiConfig in apps.py file
        """
        # Using post_save as a test signal

        u = User(username='ghjcshgdbjhcw')
        u.save()
        # self.assertTrue(True)
