# from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

from eventify_api.models import UserProfile


class UserSerializer(UserDetailsSerializer):

    company_name = serializers.CharField(source="userprofile.is_organizer")

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('is_organizer',)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        company_name = profile_data.get('is_organizer')

        instance = super(UserSerializer, self).update(instance, validated_data)

        # get and update user profile
        profile = UserProfile.objects.get_or_create(user=instance)[0]
        if profile_data and company_name:
            profile.company_name = company_name
            profile.save()
        return instance