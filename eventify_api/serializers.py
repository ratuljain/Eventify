from rest_framework import serializers
from django.forms import widgets
from eventify_api.models import Venue


class VenueSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Venue
        fields = ('id', 'venue_name', 'venue_seat_capacity',
                  'venue_latitude', 'venue_longitude',)
