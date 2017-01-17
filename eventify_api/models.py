from django.db import models


class UserProfileInformation(models.Model):
    photo_url = models.URLField()
    dob = models.DateField()
    description = models.CharField(max_length=500)
    website_url = models.URLField()
    twitter_url = models.URLField()
    facebook_url = models.URLField()


class UserSkill(models.Model):
    skill_name = models.CharField(max_length=30)
    skill_description = models.CharField(max_length=150)


class Eventify_User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=10)
    user_profile_information = models.ForeignKey(
        UserProfileInformation, on_delete=models.CASCADE)
    user_skills = models.ManyToManyField(UserSkill)
