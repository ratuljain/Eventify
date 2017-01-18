from django.db import models
from datetime import datetime


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


class Panelist(models.Model):
    user = models.OneToOneField(
        Eventify_User,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class Organiser(models.Model):
    user = models.OneToOneField(
        Eventify_User,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class EventCategory(models.Model):
    category_name = models.CharField(max_length=50)


class Venue(models.Model):
    venue_name = models.CharField(max_length=50)
    venue_seat_capacity = models.IntegerField()
    venue_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    venue_longitude = models.DecimalField(max_digits=9, decimal_places=6)


class Event(models.Model):
    event_category = models.ForeignKey(
        EventCategory, on_delete=models.CASCADE)
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE)
    agenda = models.CharField(max_length=50)
    event_name = models.CharField(max_length=50)
    event_start_time = models.DateTimeField()
    event_end_time = models.DateTimeField()
    entry_code = models.CharField(max_length=7)
    organiser = models.ManyToManyField(Organiser)
    panelist = models.ManyToManyField(Panelist)
    booking = models.ManyToManyField(Eventify_User, through='UserEventBooking')


class Attachment(models.Model):
    attachment_id = models.URLField()
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE)


class UserEventBooking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(Eventify_User, on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField(default=datetime.now, blank=True)
    booking_seat_count = models.IntegerField(default=1)
