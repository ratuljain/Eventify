from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from eventify_api import views

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^venues/$', views.VenueList.as_view(), name='venue-list'),
    url(r'^venues/(?P<pk>[0-9]+)/$', views.VenueDetail.as_view(), name='venue-detail'),
    url(r'^events/$', views.EventList.as_view(), name='event-list'),
    url(r'^events/(?P<pk>[0-9]+)/$', views.EventDetail.as_view(), name='event-detail'),
    # url(r'^eventcategory/(?P<pk>[0-9]+)/$', name='eventcategory-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
