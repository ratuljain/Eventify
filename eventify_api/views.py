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

        idtoken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjdkZjNlYmM2NmVkOGJhYjA1YTRjN2U1OTExNDM0YmVjZWU1ZTBkYmMifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vZXZlbnRpZnlhcHAtZDUxOTYiLCJuYW1lIjoiSmFuZSBRLiBVc2VyIiwicGljdHVyZSI6Imh0dHBzOi8vZXhhbXBsZS5jb20vamFuZS1xLXVzZXIvcHJvZmlsZS5qcGciLCJhdWQiOiJldmVudGlmeWFwcC1kNTE5NiIsImF1dGhfdGltZSI6MTQ4NTYxMjA2MywidXNlcl9pZCI6IjlSdVNxRHZsaXVYR0NydENpcWMzbW5wN1J2QTIiLCJzdWIiOiI5UnVTcUR2bGl1WEdDcnRDaXFjM21ucDdSdkEyIiwiaWF0IjoxNDg1NjE0MTc0LCJleHAiOjE0ODU2MTc3NzQsImVtYWlsIjoicmF0dWxqYWluMTk5MUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsicmF0dWxqYWluMTk5MUBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.RjudPbWqd-WCLMVnMKJijQ5Kl3QkIkxIhl3580p1d7rEn_t3xij9zaxWuFlTF0zTEsPtFF080nFllE7zcgFLhV3zZbkKYKVlLus4p47LILvZDe0Hcq9VcgYouWPaWpgxawJcOa3VuJqjE2xDKreo6ffJskVX_Gp_rArhrpH5CqlXszNTenBz0DOIvC0HfcdsQA_mkG5w_fzDr17od-1Uv9bLxyAZGMFz3ECjWUJPhdp6JuZuT2M6M3MDiDtKVFwAgd7N3NyX59rZmNbJ-nVXo7zaqSTr0N-DNiV85fXs7noh1Bs7I4XjhfyyQtCc__WcxUZAWWjaxsfSiX6bWZhqiA"
        target_audience = "eventifyapp-d5196"

        certificate_url = 'https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com'

        response = urllib.urlopen(certificate_url)
        certs = response.read()
        certs = json.loads(certs)

        # will throw error if not valid
        user = jwt.decode(idtoken, certs, algorithms='RS256', audience=target_audience)
        # print json.loads(user)
        return Response(user)

    def post(self, request, format=None):
        print request.data
        return Response({'key': 'value'}, status=status.HTTP_201_CREATED)