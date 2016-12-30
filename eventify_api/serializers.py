from allauth.account.utils import setup_user_email
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from allauth.utils import (email_address_exists,)
from allauth.account.adapter import get_adapter
from django.conf import settings
from eventify_api.models import UserProfile
from django.utils.translation import ugettext_lazy as _


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


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=15,
        min_length=5,
        required=True
    )
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    is_boolean = serializers.BooleanField(default=False)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if getattr(settings, "UNIQUE_EMAIL", True):
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'is_boolean': self.validated_data.get('is_boolean', '')
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
