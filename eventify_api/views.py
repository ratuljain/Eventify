from datetime import datetime, timedelta

import requests
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from jose import JWTError
from pyfcm import FCMNotification
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from eventify_api.models import Venue, Event, UserProfileInformation, UserSkill, EventifyUser, Panelist, Organiser, \
    EventCategory, EventTalk, UserEventBooking, UserEventFeedback, EventCoupon, Relationship
from eventify_api.serializers import VenueSerializer, EventSerializer, UserProfileInformationSerializer, \
    UserSkillSerializer, EventifyUserSerializer, PanelistSerializer, OrganiserSerializer, EventCategorySerializer, \
    DjangoAuthUserSerializer, EventTalkSerializer, UserEventBookingSerializer, UserEventFeedbackSerializer, \
    EventCouponsSerializer, UserConnectionSerializer, EventifyUserSerializerForConnections
from eventify_api.utils import parse_firebase_token, convertToBoolean

push_service = FCMNotification(api_key="AAAAaRIijwg:APA91bFhO7nK3uchPsKh8oo_WGzFwoL8hmfbfeWu"
                                       "_x5SBZqdm8nIcwsEAIg51qVt5l9rsajG4XlgeaBnuiUdFKoUuHve"
                                       "EEncH-2QozIA0VD2BYGhmnbnXnPjgbCHrpi3AAqK_E-RXhHGSZzaD"
                                       "D3lPhYXYffh4Pw-EQ")


def send_notification(push_service, registration_id, message_title, message_body):
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                               message_body=message_body,
                                               data_message={"id": "2", "name": "Neo4j Workshop with Django API"})

    print result


RELATIONSHIP_PENDING = 0
RELATIONSHIP_ACCEPTED = 1
RELATIONSHIP_BLOCKED = 2


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'venues': reverse('venue-list', request=request, format=format),
        'events': reverse('event-list', request=request, format=format),
        'eventify_users': reverse('eventifyuser-list', request=request, format=format),
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


class EventifyUserList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get_queryset(self):
        queryset = EventifyUser.objects.all()
        username = self.request.query_params.get('firebase_id', None)
        if username is not None:
            queryset = queryset.filter(firebase_id=username)

        return queryset

    def get(self, request, format=None):
        queryset = self.get_queryset()
        serializer = EventifyUserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventifyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        try:
            fcm_token = request.data['fcm_token']
        except KeyError:
            return Response({"error": "No fcm_token key found"}, status=status.HTTP_400_BAD_REQUEST)
        eventify_user = self.get_queryset().first()
        if eventify_user:
            eventify_user.fcm_token = fcm_token
            eventify_user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class EventifyUserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, pk):
        try:
            return EventifyUser.objects.get(pk=pk)
        except EventifyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = EventifyUserSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        print "here"
        snippet = self.get_object(pk)
        serializer = EventifyUserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

        # def patch(self, request, pk):
        #     eventify_user = self.get_object(pk)
        #     auth_user = request.data['auth_user']
        #     user_profile_information = request.data['user_profile_information']
        #
        #     phone = user_profile_information['phone']
        #     description = user_profile_information['description']
        #     employer = user_profile_information['employer']
        #     role = user_profile_information['role']
        #     website_url = user_profile_information['website_url']
        #     twitter_url = user_profile_information['twitter_url']
        #     facebook_url = user_profile_information['facebook_url']
        #
        #     user_profile = eventify_user.user_profile_information
        #     user_profile.phone = phone
        #     user_profile.description = description
        #     user_profile.employer = employer
        #     user_profile.role = role
        #     user_profile.website_url = website_url
        #     user_profile.twitter_url = twitter_url
        #     user_profile.facebook_url = facebook_url
        #
        #     user_profile.save()
        #     # set partial=True to update a data partially
        #     return Response(data={}, status=status.HTTP_201_CREATED)


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

"""
Return list of events.
Only one query param allowed.
If organiser_id is provided all the events are organized by that particular organizer are shown
If firebase_id is provided all the events attended or booked by that user are shown
If is_upcoming is provided all the events which are going to happen in the future wrt datetime.now()
will be shown
closed param can only be used in conjunction with firebase-id
"""


class EventList(APIView):

    def get(self, request, format=None):
        try:
            organiser_id = self.request.query_params.get('organiser', None)
            firebase_id = self.request.query_params.get('firebase-id', None)
            is_upcoming = self.request.query_params.get('upcoming', None)
            fields = self.request.query_params.get('fields', None)
            fields_list = None
            if fields:
                fields_list = fields.split(",")
            events = Event.objects.all()

            number_of_param = [organiser_id, firebase_id, is_upcoming]
            number_of_param = [i for i in number_of_param if i is not None]

            if len(number_of_param) > 1:
                return Response({"detail": "Only one param allowed"},
                                status=status.HTTP_400_BAD_REQUEST)

            is_closed = self.request.query_params.get('closed', None)
            is_closed = convertToBoolean(is_closed)

            if firebase_id:
                user = EventifyUser.objects.get(firebase_id=firebase_id)
                bookings = UserEventBooking.objects.filter(user=user)
                if is_closed is True:
                    events = [
                        booking.event for booking in bookings if booking.event.closed]
                else:
                    events = [booking.event for booking in bookings]
            if organiser_id:
                user = EventifyUser.objects.get(pk=organiser_id)
                organiser = Organiser.objects.get(user=user)
                nine_hours_from_now = datetime.now() + timedelta(hours=9)
                events = Event.objects.filter(
                    organiser=organiser, event_start_time__gte=nine_hours_from_now)
            if is_upcoming:
                events = Event.objects.filter(
                    event_start_time__gte=datetime.now())

            serializer = EventSerializer(events, many=True, fields=fields_list)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
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
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        Event.objects.filter(pk=pk).update(closed=True)
        event_bookings = event.usereventbooking_set.values("user")
        EventifyUser.objects.filter(id__in=event_bookings).update(blocked=True)

        return Response(status=status.HTTP_204_NO_CONTENT)


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


class UserEventFeedbackDetail(APIView):

    def get_object(self, pk):
        return get_object_or_404(UserEventFeedback, pk=pk)

    # get all feedback of an event
    def get(self, request, pk, format=None):
        feedback = self.get_object(pk)
        booking_serialized = UserEventFeedbackSerializer(
            feedback)
        return Response(booking_serialized.data)


class UserEventFeedbackList(APIView):

    def get_queryset(self):
        try:
            return UserEventFeedback.objects.all()
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        feedback = self.get_queryset()
        firebase_id = self.request.query_params.get('firebase-id', None)
        event_id = self.request.query_params.get('event-id', None)
        if event_id:
            event = get_object_or_404(Event, pk=event_id)
            feedback = feedback.filter(event=event)
        if firebase_id:
            user = get_object_or_404(EventifyUser, firebase_id=firebase_id)
            feedback = feedback.filter(user=user)
        serializer = UserEventFeedbackSerializer(feedback, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        post_data = request.data
        serializer = UserEventFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            EventifyUser.objects.filter(
                pk=post_data['user']).update(blocked=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class CouponList(generics.ListCreateAPIView):
    queryset = EventCoupon.objects.all()
    serializer_class = EventCouponsSerializer


class CouponDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventCoupon.objects.all()
    serializer_class = EventCouponsSerializer


# parameter fb_id to get friends of a user and pending requests


class ConnectionList(APIView):

    def get_user_by_FUID(self):
        firebase_id = self.request.query_params.get('firebase-id', None)
        eventify_user = None
        if firebase_id is not None:
            eventify_user = get_object_or_404(
                EventifyUser, firebase_id=firebase_id)

        return eventify_user

    def get_queryset(self):
        try:
            return Relationship.objects.all()
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        response_map = {}
        # response = {}
        pending_relationships_res = []
        accepted_relationships_res = []
        blocked_relationships_res = []
        firebase_id = self.request.query_params.get('firebase-id', None)

        user_connections = self.get_queryset()
        serializer = UserConnectionSerializer(
            user_connections, many=True, context={'request': request})
        response = serializer.data

        # TODO please make this better when you get time
        if firebase_id:
            eventify_user = get_object_or_404(
                EventifyUser, firebase_id=firebase_id)

            pending_relationships = Relationship.objects.filter(
                to_person=eventify_user, status=RELATIONSHIP_PENDING)
            accepted_relationships = Relationship.objects.filter(Q(to_person=eventify_user) | Q(
                from_person=eventify_user), status=RELATIONSHIP_ACCEPTED)
            accepted_relationships_custom_serialized = filter_stuff(
                request, accepted_relationships, eventify_user)

            blocked_relationships = eventify_user.get_relationships(
                RELATIONSHIP_BLOCKED)
            for i in blocked_relationships:
                blocked_relationships_res.append(Relationship.objects.get(
                    from_person=eventify_user, to_person=i))

            response_map["pending_relationships"] = UserConnectionSerializer(pending_relationships, many=True,
                                                                             context={'request': request}).data
            response_map[
                "accepted_relationships"] = accepted_relationships_custom_serialized
            response_map["blocked_relationships"] = UserConnectionSerializer(blocked_relationships_res, many=True,
                                                                             context={'request': request}).data
            return Response(data=response_map, status=status.HTTP_200_OK)

        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        request_from = self.request.query_params.get('from', None)
        request_to = self.request.query_params.get('to', None)
        event_id = self.request.query_params.get('event-id', None)

        if None in [request_from, request_to, event_id]:
            return Response(data={'error': 'request_from, request_to, event_id parms are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        from_user = get_object_or_404(EventifyUser, firebase_id=request_from)
        to_user = get_object_or_404(EventifyUser, firebase_id=request_to)
        event = get_object_or_404(Event, pk=event_id)

        # TODO change this validation
        results1 = Relationship.objects.filter(
            from_person=from_user, to_person=to_user)
        results2 = Relationship.objects.filter(
            from_person=to_user, to_person=from_user)
        num_results1 = len(results1)
        num_results2 = len(results2)

        if num_results1 + num_results2 == 1:
            return Response(data={'error': 'Connection Pending/Exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        user_connection = from_user.add_relationship(
            to_user, RELATIONSHIP_PENDING, event)
        serializer = UserConnectionSerializer(
            user_connection, context={'request': request})

        from_user_first_name = from_user.auth_user.first_name
        from_user_last_name = from_user.auth_user.last_name

        message_title = "New Connection"
        message_body = "{} {} wants to connect to you".format(
            from_user_first_name, from_user_last_name)

        send_notification(push_service, to_user.fcm_token,
                          message_title, message_body)
        # send_notification(push_service, to_user.fcm_token,
        #                   message_title, message_body)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, format=None):
        request_from = self.request.query_params.get('from', None)
        request_to = self.request.query_params.get('to', None)
        event_id = self.request.query_params.get('event-id', None)

        if None in [request_from, request_to, event_id]:
            return Response(data={'error': 'request_from, request_to, event_id parms are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        from_user = get_object_or_404(EventifyUser, firebase_id=request_from)
        to_user = get_object_or_404(EventifyUser, firebase_id=request_to)
        event = get_object_or_404(Event, pk=event_id)

        user_connection = from_user.update_relationship(
            to_user, RELATIONSHIP_ACCEPTED)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, format=None):
        request_from = self.request.query_params.get('from', None)
        request_to = self.request.query_params.get('to', None)
        event_id = self.request.query_params.get('event-id', None)

        if None in [request_from, request_to, event_id]:
            return Response(data={'error': 'request_from, request_to, event_id parms are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        from_user = get_object_or_404(EventifyUser, firebase_id=request_from)
        to_user = get_object_or_404(EventifyUser, firebase_id=request_to)
        event = get_object_or_404(Event, pk=event_id)

        user_connection = from_user.update_relationship(
            to_user, RELATIONSHIP_BLOCKED, event)
        print user_connection

        return Response(status=status.HTTP_204_NO_CONTENT)


class FirebaseToken(APIView):
    # def get(self, request, format=None):
    #     return Response({})

    def post(self, request, format=None):
        id_token = request.data['id_token']

        try:
            response_body = parse_firebase_token(id_token)
            # print response_body
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


def filter_stuff(request, accepted_relationships, user):
    res = []
    for relationship_object in accepted_relationships:
        from_to_tuple = [relationship_object.from_person.pk,
                         relationship_object.to_person.pk]
        x = set(from_to_tuple) - {user.pk}
        user_connection = EventifyUser.objects.get(pk=x.pop())
        serialized_user = EventifyUserSerializerForConnections(
            user_connection, context={'request': request}).data
        _serialized_relationship = UserConnectionSerializer(
            relationship_object, context={'request': request}).data
        serialized_relationship = dict(_serialized_relationship)
        serialized_relationship['to_person'] = serialized_user
        del serialized_relationship['from_person']
        res.append(serialized_relationship)

    return res


class CloudinaryPictures(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        prefix_text = 'Eventify/' + str(event.pk)
        payload = {'prefix': prefix_text, 'max_results': '50'}
        r = requests.get('https://api.cloudinary.com/v1_1/dukt9s7aj/resources/image/upload',
                         auth=('742926962481883', 'MQ5RQj650yZcaIhxC1IYcbnvSxg'), params=payload)
        try:
            r.raise_for_status()
            status = r.status_code
        except:
            status = r.status_code

        data = r.json()

        return Response(data=data, status=status)
