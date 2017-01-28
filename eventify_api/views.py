from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from eventify_api.models import Venue, Event, UserProfileInformation, UserSkill, EventifyUser, Panelist, Organiser, \
    EventCategory
from eventify_api.serializers import VenueSerializer, EventSerializer, UserProfileInformationSerializer, \
    UserSkillSerializer, EventifyUserSerializer, PanelistSerializer, OrganiserSerializer, EventCategorySerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'stops': reverse('venue-list', request=request, format=format),
        'events': reverse('event-list', request=request, format=format),
    })


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
    queryset = EventifyUser.objects.all()
    serializer_class = EventifyUserSerializer


class EventifyUserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = EventifyUser.objects.all()
    serializer_class = EventifyUserSerializer


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


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class FirebaseToken(APIView):
    def get(self, request, format=None):
        import urllib, json
        from jose import jwt

        idtoken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjdkZjNlYmM2NmVkOGJhYjA1YTRjN2U1OTExNDM0YmVjZWU1ZTBkYmMifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXZlbnRpZnlhcHAtZDUxOTYiLCJuYW1lIjoiSmFuZSBRLiBVc2VyIiwicGljdHVyZSI6Imh0dHBzOi8vZXhhbXBsZS5jb20vamFuZS1xLXVzZXIvcHJvZmlsZS5qcGciLCJhdWQiOiJldmVudGlmeWFwcC1kNTE5NiIsImF1dGhfdGltZSI6MTQ4NTYxNzY3MCwidXNlcl9pZCI6IjlSdVNxRHZsaXVYR0NydENpcWMzbW5wN1J2QTIiLCJzdWIiOiI5UnVTcUR2bGl1WEdDcnRDaXFjM21ucDdSdkEyIiwiaWF0IjoxNDg1NjE3OTA4LCJleHAiOjE0ODU2MjE1MDgsImVtYWlsIjoicmF0dWxqYWluMTk5MUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF0dWxqYWluMTk5MUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.xkUpxRrdm4gHmgTBxjJ5V3ZoXIIXc1ycQKft2yVDre0UP-hUdetBRgeFjR8f1koTd7bnUPHtIckWIOgVOXcXWt5td7Z38DN2vfXAMbSftxYIRmWkizK-C7kANnzspAFE1jzKadU3Jr1gRp_LAYt8GI3C07zUeMdngm-qWm7xifVcce9KQjBUSzv549ka6RaaqAbuhf2f1c75w2CuDeyVMVxOreVSUG2ZZa1m7YnLTi03_Fp4Tl4fN0wIAZ8Zp4MNjHf77Jko_IPzMqXrl7gdcyCzvtDtH00a1_VSqsfVPqTgeyI5lsKfx8QeUT43IgoKKOsKx9CoUY_fKg3TiA3uyg"
        target_audience = "eventifyapp-d5196"

        certificate_url = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'

        response = urllib.urlopen(certificate_url)
        certs = response.read()
        certs = json.loads(certs)

        # will throw error if not valid
        user = jwt.decode(idtoken, certs, algorithms='RS256', audience=target_audience)

        import sys, time

        for a in range(1, 11):
            sys.stdout.write('\r {0} files processed.'.format(a))
            time.sleep(.1)

        print('')
        sys.stdout.write('\r#####                     (33%)')
        time.sleep(1)
        sys.stdout.write('\r#############             (66%)')
        time.sleep(1)
        sys.stdout.write('\r#######################   (100%)')
        print('')

        # print json.loads(user)
        return Response(user)

    def post(self, request, format=None):
        print request.data
        return Response({'key': 'value'}, status=status.HTTP_201_CREATED)