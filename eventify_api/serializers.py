from django.contrib.auth.models import User
from rest_framework import serializers

from eventify_api.models import Event, Venue, UserSkill, EventifyUser, UserProfileInformation, Panelist, Organiser, \
    EventCategory, EventTalk, Attachment, UserEventBooking, UserEventFeedback


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
                  'description', 'sex', 'employer', 'role',
                  'website_url', 'twitter_url', 'facebook_url', 'user_skills',)

        depth = 1


class EventifyUserSerializer(serializers.ModelSerializer):
    auth_user = DjangoAuthUserSerializer()
    user_profile_information = UserProfileInformationSerializer()

    class Meta:
        model = EventifyUser
        fields = ('id', 'auth_user', 'firebase_id', 'fcm_token',
                  'user_profile_information',)
        depth = 2

    def create(self, validated_data):
        auth_user_data = validated_data.pop('auth_user')
        user_profile_information_data = validated_data.pop(
            'user_profile_information')
        eventifyUser = EventifyUser.objects.create(
            firebase_id=validated_data['firebase_id'])
        user_profile_information = None

        auth_user = User.objects.update_or_create(**auth_user_data)
        if auth_user.pk:
            user_profile_information = UserProfileInformation.objects.update_or_create(
                **user_profile_information_data)
        if auth_user.pk and user_profile_information:
            eventifyUser.auth_user = auth_user
            eventifyUser.user_profile_information = user_profile_information
            eventifyUser.save()
        return eventifyUser


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


class UserEventFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEventFeedback
        fields = ('event', 'user', 'rating', 'feedback_text',
                  'food', 'panelist', 'relevance',
                  'engagement', 'duration', 'crowd',)


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
            'entry_code', 'organiser', 'panelist', 'talks',)
        depth = 4
