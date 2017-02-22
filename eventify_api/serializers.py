from django.contrib.auth.models import User
from rest_framework import serializers

from eventify_api.models import Event, Venue, UserSkill, EventifyUser, UserProfileInformation, Panelist, Organiser, \
    EventCategory, EventTalk, Attachment, UserEventBooking


class DjangoAuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'date_joined',)
        depth = 1


class UserProfileInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfileInformation
        fields = ('id', 'photo_url', 'phone', 'dob',
                  'description', 'website_url', 'twitter_url', 'facebook_url', 'user_skills',)


class EventifyUserSerializer(serializers.ModelSerializer):
    # user_profile_information = serializers.HyperlinkedRelatedField(
    #     view_name='userprofileinformation-detail', read_only=True)
    # user_skills = serializers.HyperlinkedRelatedField(
    #     many=True, view_name='userskills-detail', read_only=True)
    auth_user = DjangoAuthUserSerializer()

    class Meta:
        model = EventifyUser
        fields = ('id', 'auth_user', 'firebase_id',
                  'user_profile_information',)
        depth = 2


class UserSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSkill
        fields = ('id', 'skill_name', 'skill_description',)


class PanelistSerializer(serializers.ModelSerializer):
    user = EventifyUserSerializer()

    class Meta:
        model = Panelist
        fields = ('user',)


class OrganiserSerializer(serializers.ModelSerializer):
    user = EventifyUserSerializer()

    class Meta:
        model = Organiser
        fields = ('user',)


class UserEventBookingSerializer(serializers.ModelSerializer):
    user = EventifyUserSerializer()

    class Meta:
        model = UserEventBooking
        fields = ('user', 'booking_datetime',
                  'booking_seat_count', 'pin_verified', )


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory
        fields = ('id', 'category_name',)


class VenueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'venue_seat_capacity', 'location',
                  'venue_latitude', 'venue_longitude', 'venue_latitude_str',
                  'venue_longitude_str')


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = ('id', 'file', 'attachment_url',
                  'file_name',)


class EventTalkSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventTalk
        fields = ('id', 'talk_name', 'talk_description',
                  'talk_start_time', 'talk_end_time', 'talks_attachments',)
        depth = 1


class EventSerializer(serializers.ModelSerializer):
    panelist = PanelistSerializer(many=True, read_only=True)
    organiser = OrganiserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'event_bg_image', 'event_category', 'venue', 'agenda',
            'event_name', 'event_start_time', 'event_end_time',
            'entry_code', 'organiser', 'panelist', 'talks', 'booking')
        depth = 4
