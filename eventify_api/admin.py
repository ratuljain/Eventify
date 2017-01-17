from django.contrib import admin
from eventify_api.models import Eventify_User, UserSkill, UserProfileInformation


class Eventify_UserAdmin(admin.ModelAdmin):
    pass


class UserSkillAdmin(admin.ModelAdmin):
    pass


class UserProfileInformationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Eventify_User, Eventify_UserAdmin)
admin.site.register(UserSkill, UserSkillAdmin)
admin.site.register(UserProfileInformation, UserProfileInformationAdmin)
