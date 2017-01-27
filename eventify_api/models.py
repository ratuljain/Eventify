from datetime import datetime

from django.db import models


class UserProfileInformation(models.Model):
    photo_url = models.URLField()
    dob = models.DateField()
    description = models.CharField(max_length=500)
    website_url = models.URLField()
    twitter_url = models.URLField()
    facebook_url = models.URLField()

    def __unicode__(self):
        return self.photo_url


class UserSkill(models.Model):
    skill_name = models.CharField(max_length=30)
    skill_description = models.CharField(max_length=150)

    def __unicode__(self):
        return self.skill_name


class EventifyUser(models.Model):
    firebase_id = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=10)
    user_profile_information = models.OneToOneField(
        UserProfileInformation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user_skills = models.ManyToManyField(UserSkill, blank=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Panelist(models.Model):
    user = models.OneToOneField(
        EventifyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


class Organiser(models.Model):
    user = models.OneToOneField(
        EventifyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name


class EventCategory(models.Model):
    category_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.category_name


class Venue(models.Model):
    venue_name = models.CharField(max_length=50)
    venue_seat_capacity = models.IntegerField()
    venue_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    venue_longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __unicode__(self):
        return self.venue_name


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
    booking = models.ManyToManyField(EventifyUser, through='UserEventBooking')

    def __unicode__(self):
        return self.event_name


class EventTalk(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    talk_name = models.CharField(max_length=100)
    talk_datetime = models.DateTimeField(default=datetime.now, blank=True)
    session = models.ManyToManyField(
        Panelist, through='UserPanelistSession')

    def __unicode__(self):
        return self.event.event_name + " - " + self.talk_name


class UserPanelistSession(models.Model):
    event_talk = models.ForeignKey(
        EventTalk, on_delete=models.CASCADE)
    event_attendee = models.ForeignKey(EventifyUser, on_delete=models.CASCADE)
    event_panelist = models.ForeignKey(Panelist, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.event_attendee.first_name + " - " + self.event_panelist.user.first_name


class Attachment(models.Model):
    attachment_url = models.URLField()
    event_talk = models.ForeignKey(
        EventTalk, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.attachment_id


class UserEventBooking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(EventifyUser, on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField(default=datetime.now, blank=True)
    booking_seat_count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.event.event_name + " - " + self.user.first_name


class Question(models.Model):
    by_user = models.ForeignKey(EventifyUser, on_delete=models.CASCADE)
    event_talk = models.ForeignKey(
        EventTalk, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=250)
    answer_text = models.CharField(max_length=250)

    def __unicode__(self):
        return self.event.question_text
