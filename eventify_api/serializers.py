from django.contrib.auth.models import User
from rest_framework import serializers

from eventify_api.models import Event, Venue, UserSkill, EventifyUser, UserProfileInformation, Panelist, Organiser, \
    EventCategory


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
    user = DjangoAuthUserSerializer()

    class Meta:
        model = EventifyUser
        fields = ('id', 'user', 'firebase_id', 'user_profile_information',)
        depth = 1


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


class EventCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCategory
        fields = ('id', 'category_name',)


class VenueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'venue_seat_capacity',
                  'venue_latitude', 'venue_longitude',)


class EventSerializer(serializers.ModelSerializer):
    panelist = PanelistSerializer(many=True, read_only=True)
    organiser = OrganiserSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'event_bg_image', 'event_category', 'venue', 'agenda',
            'event_name', 'event_start_time', 'event_end_time',
            'entry_code', 'organiser', 'panelist',)
        depth = 2
