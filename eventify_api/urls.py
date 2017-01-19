from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from eventify_api import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^venues/$', views.VenueList.as_view(), name='venue-list'),
    url(r'^venues/(?P<pk>[0-9]+)/$', views.VenueDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
