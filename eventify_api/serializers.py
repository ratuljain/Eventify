from django.contrib.auth.models import User
from rest_framework import serializers

from eventify_api.models import Event, Venue, UserSkill, EventifyUser, UserProfileInformation, Panelist, Organiser, \
    EventCategory, EventTalk, Attachment, UserEventBooking, UserEventFeedback, EventCoupon, Relationship


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class DjangoAuthUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'date_joined',)
        depth = 1


class UserProfileInformationSerializer(serializers.ModelSerializer):
    user_skills_comma_separated_string = serializers.SerializerMethodField()

    class Meta:
        model = UserProfileInformation
        fields = ('id', 'photo_url', 'phone', 'dob',
                  'description', 'sex', 'employer', 'role',
                  'website_url', 'twitter_url', 'facebook_url', 'user_skills', 'user_skills_comma_separated_string',)

        depth = 1

    def get_user_skills_comma_separated_string(self, obj):
        return ", ".join(obj.user_skills.all().values_list("skill_name", flat=True))


class EventifyUserSerializer(serializers.ModelSerializer):
    auth_user = DjangoAuthUserSerializer(required=False)
    user_profile_information = UserProfileInformationSerializer(required=True)
    # connection = UserConnectionSerializer()

    class Meta:
        model = EventifyUser
        fields = ('id', 'auth_user', 'firebase_id', 'fcm_token', 'blocked',
                  'user_profile_information',)
        depth = 2

    def create(self, validated_data):
        auth_user_data = validated_data.pop('auth_user')
        user_profile_information_data = validated_data.pop(
            'user_profile_information')
        eventifyUser = EventifyUser.objects.create(
            firebase_id=validated_data['firebase_id'])
        user_profile_information = None

        auth_user, created = User.objects.update_or_create(**auth_user_data)
        user_profile_information, created = UserProfileInformation.objects.update_or_create(
            **user_profile_information_data)
        eventifyUser.auth_user = auth_user
        eventifyUser.user_profile_information = user_profile_information
        eventifyUser.save()
        return eventifyUser

    def update(self, instance, validated_data):
        print instance
        return instance


class EventifyUserSerializerForConnections(serializers.ModelSerializer):
    # connection = UserConnectionSerializer()
    first_name = serializers.ReadOnlyField(source='auth_user.first_name')
    last_name = serializers.ReadOnlyField(source='auth_user.last_name')

    class Meta:
        model = EventifyUser
        fields = ('id', 'first_name', 'last_name', 'firebase_id', 'fcm_token', 'blocked',
                  'user_profile_information',)
        depth = 0


class UserConnectionSerializer(serializers.HyperlinkedModelSerializer):
    # initiated_by_user = EventifyUserSerializer()
    # sent_to_user = EventifyUserSerializer()
    # from_person = EventifyUserSerializerForConnections()
    from_person = EventifyUserSerializerForConnections()
    event = serializers.ReadOnlyField(source='event.id')
    event_name = serializers.ReadOnlyField(source='event.event_name')
    met_time = serializers.ReadOnlyField(source='event.event_start_time')

    class Meta:
        model = Relationship
        fields = ('id', 'from_person', 'event_name', 'met_time',
                  'event', 'status',)
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


class UserEventBookingSerializer(DynamicFieldsModelSerializer):
    user = EventifyUserSerializer()

    class Meta:
        model = UserEventBooking
        fields = ('user', 'booking_datetime',
                  'booking_seat_count', 'pin_verified', )


class UserEventFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserEventFeedback
        fields = ('id', 'event', 'user', 'rating', 'feedback_text',
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


class EventCouponsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventCoupon
        fields = ('id', 'provider_name', 'coupon_description',
                  'coupon_url',)
        depth = 1


class EventSerializer(DynamicFieldsModelSerializer):
    panelist = PanelistSerializer(many=True, read_only=True)
    organiser = OrganiserSerializer(many=True, read_only=True)
    coupons = EventCouponsSerializer(many=True, read_only=True)
    talks = EventTalkSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id', 'event_bg_image', 'event_category', 'venue', 'agenda',
            'event_name', 'event_start_time', 'event_end_time',
            'entry_code', 'organiser', 'panelist', 'talks', 'closed', 'coupons',)
        depth = 4
