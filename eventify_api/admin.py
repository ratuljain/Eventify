from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from eventify_api.models import EventifyUser, UserSkill, UserProfileInformation, \
    Panelist, Organiser, EventCategory, Venue, Attachment, Event, UserEventBooking, EventTalk, UserPanelistSession, \
    UserEventFeedback, EventCoupon, Relationship


class UserConnectionInline(admin.TabularInline):
    model = Relationship
    fk_name = 'from_person'


class UserConnectionAdmin(admin.ModelAdmin):
    model = Relationship
    fk_name = 'from_person'


class Eventify_UserAdmin(admin.ModelAdmin):
    model = EventifyUser
    inlines = [UserConnectionInline]


class UserSkillAdmin(admin.ModelAdmin):
    pass


class EventCouponAdmin(admin.ModelAdmin):
    pass


class UserFeedbackAdmin(admin.ModelAdmin):
    pass


class UserProfileInformationAdmin(admin.ModelAdmin):
    pass


class PanelistAdmin(admin.ModelAdmin):
    pass


class OrganiserAdmin(admin.ModelAdmin):
    pass


class EventCategoryAdmin(admin.ModelAdmin):
    pass


class VenueAdmin(admin.ModelAdmin):
    pass


class AttachmentAdmin(admin.ModelAdmin):
    pass


class UserEventBookingInline(admin.TabularInline):
    model = UserEventBooking


class EventTalkInline(admin.TabularInline):
    model = EventTalk
    max_num = 3


class EventFeedbackInline(admin.TabularInline):
    model = UserEventFeedback


class EventAdmin(admin.ModelAdmin):
    model = Event
    inlines = [UserEventBookingInline, EventTalkInline, EventFeedbackInline]


class UserPanelistSessionInline(admin.TabularInline):
    model = UserPanelistSession


class EventTalkAdmin(admin.ModelAdmin):
    model = EventTalk
    inlines = [UserPanelistSessionInline]


class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(EventifyUser, Eventify_UserAdmin)
admin.site.register(UserSkill, UserSkillAdmin)
admin.site.register(EventCoupon, EventCouponAdmin)
admin.site.register(UserEventFeedback, UserFeedbackAdmin)
admin.site.register(UserProfileInformation, UserProfileInformationAdmin)
admin.site.register(Panelist, PanelistAdmin)
admin.site.register(Organiser, OrganiserAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventTalk, EventTalkAdmin)
admin.site.unregister(User,)
admin.site.register(User, UserAdmin)
admin.site.register(Relationship, UserConnectionAdmin)
