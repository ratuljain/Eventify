import random
import string

from django.contrib.auth.models import User
from django.http import Http404
from jose import JWTError
from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from eventify_api.models import Venue, Event, UserProfileInformation, UserSkill, EventifyUser, Panelist, Organiser, \
    EventCategory, EventTalk, UserEventBooking, UserEventFeedback
from eventify_api.serializers import VenueSerializer, EventSerializer, UserProfileInformationSerializer, \
    UserSkillSerializer, EventifyUserSerializer, PanelistSerializer, OrganiserSerializer, EventCategorySerializer, \
    DjangoAuthUserSerializer, EventTalkSerializer, UserEventBookingSerializer, UserEventFeedbackSerializer
from eventify_api.utils import parse_firebase_token


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'stops': reverse('venue-list', request=request, format=format),
        'events': reverse('event-list', request=request, format=format),
    })


class AuthUserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = DjangoAuthUserSerializer


class AuthUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = DjangoAuthUserSerializer


class UserProfileInformationList(generics.ListCreateAPIView):
    queryset = UserProfileInformation.objects.all()
    serializer_class = UserProfileInformationSerializer


class UserProfileInformationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfileInformation.objects.all()
    serializer_class = UserProfileInformationSerializer


class UserSkillList(generics.ListCreateAPIView):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer


class UserSkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer


class EventifyUserList(generics.ListCreateAPIView):

    def get_queryset(self):
        """

        """
        queryset = EventifyUser.objects.all()
        username = self.request.query_params.get('firebase_id', None)
        if username is not None:
            queryset = queryset.filter(firebase_id=username)
        return queryset

    serializer_class = EventifyUserSerializer


class EventifyUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventifyUser.objects.all()
    serializer_class = EventifyUserSerializer


# class EventifyUserDetailFireBaseID(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#
#     def get_object(self, pk):
#         try:
#             print pk
#             return EventifyUser.objects.get(firebase_id=pk)
#         except EventifyUser.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         snippet = self.get_object(pk)
#         serializer = EventifyUserSerializer(snippet)
#         return Response(serializer.data)


class PanelistList(generics.ListCreateAPIView):
    queryset = Panelist.objects.all()
    serializer_class = PanelistSerializer


class PanelistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Panelist.objects.all()
    serializer_class = PanelistSerializer


class OrganiserList(generics.ListCreateAPIView):
    queryset = Organiser.objects.all()
    serializer_class = OrganiserSerializer


class OrganiserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organiser.objects.all()
    serializer_class = OrganiserSerializer


class EventCategoryList(generics.ListCreateAPIView):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer


class EventCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer


class VenueList(generics.ListCreateAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class VenueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class EventTalkList(generics.ListCreateAPIView):
    queryset = EventTalk.objects.all()
    serializer_class = EventTalkSerializer


class EventTalkDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventTalk.objects.all()
    serializer_class = EventTalkSerializer


# class EventList(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer


class EventList(APIView):
    def get(self, request, format=None):
        try:
            organiser_id = self.request.query_params.get('organiser', None)
            events = Event.objects.all()

            if organiser_id:
                user = EventifyUser.objects.get(pk=organiser_id)
                organiser = Organiser.objects.get(user=user)
                events = Event.objects.filter(organiser=organiser)

            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
        except EventifyUser.DoesNotExist:
            raise Http404
        except Organiser.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetail(APIView):

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        # event_bookings = event.usereventbooking_set.all()
        # booking_serialized = UserEventBookingSerializer(
        #     event_bookings, many=True)
        serializer = EventSerializer(event)
        # serializer.data['booking'] = booking_serialized.data
        return Response(serializer.data)


class UserEventBookingDetailList(generics.ListCreateAPIView):
    queryset = UserEventBooking.objects.all()
    serializer_class = UserEventBookingSerializer


class UserEventBookingDetail(APIView):

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        event_bookings = event.usereventbooking_set.all()

        pin_verified = self.request.query_params.get('verified', None)
        if pin_verified is not None:
            event_bookings = event_bookings.filter(pin_verified=pin_verified)

        booking_serialized = UserEventBookingSerializer(
            event_bookings, many=True)
        return Response(booking_serialized.data)


class UserEventFeedbackList(APIView):

    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        event_bookings = event.usereventfeedback_set.all()
        booking_serialized = UserEventFeedbackSerializer(
            event_bookings, many=True)
        return Response(booking_serialized.data)


class UserEventFeedbackDetail(generics.ListCreateAPIView):
    queryset = UserEventFeedback.objects.all()
    serializer_class = UserEventFeedbackSerializer


# class UserEventFeedbackDetail(APIView):
#
#     def get(self, request, event_pk, firebase_uid, format=None):
#         try:
#             event = Event.objects.get(pk=event_pk)
#             user = EventifyUser.objects.get(firebase_id=firebase_uid)
#             user_booking_status = {}
#
#             user_feedback = UserEventFeedback.objects.get(event=event, user=user)
#
#             booking_serialized = UserEventFeedbackSerializer(user_feedback)
#             return Response(data=booking_serialized.data, status=status.HTTP_200_OK)
#
#         except Event.DoesNotExist:
#             raise Http404
#         except EventifyUser.DoesNotExist:
#             raise Http404
#         except UserEventFeedback.DoesNotExist:
#             raise Http404
#
#     def post(self, request, event_pk, firebase_uid, format=None):
#         try:
#             event = Event.objects.get(pk=event_pk)
#             user = EventifyUser.objects.get(firebase_id=firebase_uid)
#             user_booking_status = {}
#
#             user_feedback = UserEventFeedback.objects.get(event=event, user=user)
#
#             booking_serialized = UserEventFeedbackSerializer(user_feedback)
#             return Response(data=booking_serialized.data, status=status.HTTP_200_OK)
#
#         except Event.DoesNotExist:
#             raise Http404
#         except EventifyUser.DoesNotExist:
#             raise Http404
#         except UserEventFeedback.DoesNotExist:
#             raise Http404


"""
Endpoint to check if pin entered by the user for an event
is correct. Toggle verifed filed depending on the result.
"""


class ToggleUserEventBookingPinVerified(APIView):
    """
    ENDPOINT TO CHECK STATUS OF A BOOKING.
    {
        "booked": boolean,
        "verified": boolean
    }
    """

    def get(self, request, event_pk, firebase_uid, format=None):
        try:
            event = Event.objects.get(pk=event_pk)
            user = EventifyUser.objects.get(firebase_id=firebase_uid)
            user_booking_status = {}

            booking_info = UserEventBooking.objects.get(event=event, user=user)
            user_booking_status['booked'] = True
            user_booking_status['verified'] = booking_info.pin_verified

            return Response(data=user_booking_status, status=status.HTTP_200_OK)

        except Event.DoesNotExist:
            raise Http404
        except UserEventBooking.DoesNotExist:
            raise Http404

    def post(self, request, event_pk, firebase_uid, format=None):

        try:
            event = Event.objects.get(pk=event_pk)
            user = EventifyUser.objects.get(firebase_id=firebase_uid)

            UserEventBooking.objects.get_or_create(event=event, user=user)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            raise Http404
        except UserEventBooking.DoesNotExist:
            raise Http404

    def put(self, request, event_pk, firebase_uid, format=None):

        try:
            event = Event.objects.get(pk=event_pk)
            user = EventifyUser.objects.get(firebase_id=firebase_uid)
            event_bookings = event.usereventbooking_set.get(user=user)
            event_bookings.pin_verified = True
            # event_bookings.pin_verified = request.data['pin_verified']
            event_bookings.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            raise Http404
        except UserEventBooking.DoesNotExist:
            raise Http404

    def delete(self, request, event_pk, firebase_uid, format=None):

        try:
            event = Event.objects.get(pk=event_pk)
            user = EventifyUser.objects.get(firebase_id=firebase_uid)
            event_bookings = event.usereventbooking_set.get(user=user)
            event_bookings.pin_verified = False
            # event_bookings.pin_verified = request.data['pin_verified']
            event_bookings.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Event.DoesNotExist:
            raise Http404
        except UserEventBooking.DoesNotExist:
            raise Http404


class FirebaseToken(APIView):
    # def get(self, request, format=None):
    #     return Response({})

    def post(self, request, format=None):
        id_token = request.data['id_token']

        try:
            response_body = parse_firebase_token(id_token)
            print response_body
            user_id = str(response_body['user_id'])
            username = response_body['email']
            name = response_body['name']

            try:
                user = EventifyUser.objects.get(firebase_id=user_id)
                eventify_auth_user = user.auth_user
                if eventify_auth_user.first_name != name:
                    eventify_auth_user.first_name = name
                    eventify_auth_user.save()

            except EventifyUser.DoesNotExist:
                user, created = User.objects.get_or_create(
                    username=username, email=username, first_name=name)
                # user.set_password(user_id)
                eventify_user = EventifyUser(
                    auth_user=user, firebase_id=user_id)
                eventify_user.save()
            request_status = status.HTTP_200_OK
        except JWTError:
            response_body = {"id_token": "Signature verification failed."}
            request_status = status.HTTP_401_UNAUTHORIZED

        return Response(data=response_body, status=request_status)
