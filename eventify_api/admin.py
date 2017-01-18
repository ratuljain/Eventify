from django.contrib import admin
from eventify_api.models import Eventify_User, UserSkill, UserProfileInformation, \
    Panelist, Organiser, EventCategory, Venue, Attachment, Event, UserEventBooking


class Eventify_UserAdmin(admin.ModelAdmin):
    pass


class UserSkillAdmin(admin.ModelAdmin):
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


class EventAdmin(admin.ModelAdmin):
    pass


class UserEventBookingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Eventify_User, Eventify_UserAdmin)
admin.site.register(UserSkill, UserSkillAdmin)
admin.site.register(UserProfileInformation, UserProfileInformationAdmin)
admin.site.register(Panelist, PanelistAdmin)
admin.site.register(Organiser, OrganiserAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(UserEventBooking, UserEventBookingAdmin)
