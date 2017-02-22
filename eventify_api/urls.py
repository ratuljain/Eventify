from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_nested import routers

from eventify_api import views


urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^users/$', views.AuthUserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.AuthUserDetail.as_view(), name='user-detail'),
    url(r'^venues/$', views.VenueList.as_view(), name='venue-list'),
    url(r'^venues/(?P<pk>[0-9]+)/$',
        views.VenueDetail.as_view(), name='venue-detail'),
    url(r'^events/$', views.EventList.as_view(), name='event-list'),
    url(r'^events/(?P<pk>[0-9]+)/$',
        views.EventDetail.as_view(), name='event-detail'),
    url(r'^profileinformations/$', views.UserProfileInformationList.as_view(),
        name='userprofileinformation-list'),
    url(r'^profileinformations/(?P<pk>[0-9]+)/$', views.UserProfileInformationDetail.as_view(
    ), name='userprofileinformation-detail'),
    url(r'^userskills/$', views.UserSkillList.as_view(), name='userskills-list'),
    url(r'^userskills/(?P<pk>[0-9]+)/$',
        views.UserSkillDetail.as_view(), name='userskills-detail'),
    url(r'^eventifyusers/$', views.EventifyUserList.as_view(),
        name='eventifyuser-list'),
    # url(r'^uid/(?P<pk>(.+))/$', views.EventifyUserDetailFireBaseID.as_view(),
    #     name='eventifyuserfuid-list'),
    url(r'^eventifyusers/(?P<pk>[0-9]+)/$',
        views.EventifyUserDetail.as_view(), name='eventifyuser-detail'),
    url(r'^panelists/$', views.PanelistList.as_view(), name='panelist-list'),
    url(r'^panelists/(?P<pk>[0-9]+)/$',
        views.PanelistDetail.as_view(), name='panelist-detail'),
    url(r'^organisers/$', views.OrganiserList.as_view(), name='organiser-list'),
    url(r'^organisers/(?P<pk>[0-9]+)/$',
        views.OrganiserDetail.as_view(), name='organiser-detail'),
    url(r'^talks/$', views.EventTalkList.as_view(), name='organiser-list'),
    url(r'^talks/(?P<pk>[0-9]+)/$',
        views.EventTalkDetail.as_view(), name='organiser-detail'),
    url(r'^eventcategories/$', views.EventTalkDetail.as_view(),
        name='organiser-list'),
    url(r'^eventcategories/(?P<pk>[0-9]+)/$',
        views.EventCategoryDetail.as_view(), name='organiser-detail'),
    url(r'^firebase-token/$', views.FirebaseToken.as_view(),
        name='firebase-token'),
    url(r'^bookings/$', views.UserEventBookingDetailList.as_view(),
        name='booking-list'),
    url(r'^bookings/(?P<pk>[0-9]+)/$',
        views.UserEventBookingDetail.as_view(), name='booking-detail'),
    url(r'^verifyuser/event/(?P<event_pk>[0-9]+)/user/(?P<firebase_uid>(.)+)/$',
        views.ToggleUserEventBookingPinVerified.as_view(), name='booking-verify'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
