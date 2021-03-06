from datetime import datetime

from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from places.fields import PlacesField


RELATIONSHIP_PENDING = 0
RELATIONSHIP_ACCEPTED = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_PENDING, 'Pending'),
    (RELATIONSHIP_ACCEPTED, 'Accepted'),
    (RELATIONSHIP_BLOCKED, 'Blocked'),
)


class IntegerRangeField(models.IntegerField):

    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class UserSkill(models.Model):
    skill_name = models.CharField(max_length=30)
    skill_description = models.CharField(max_length=150)

    def __unicode__(self):
        return self.skill_name


class UserProfileInformation(models.Model):
    SEX_CHOICES = (
        ('Female', 'Female',),
        ('Male', 'Male',),
    )
    ROLE_CHOICES = (
        ('Developer', 'Developer',),
        ('Tester', 'Tester',),
        ('Manager', 'Manager',),
        ('Student', 'Student',),
    )
    photo_url = models.URLField()
    phone = models.CharField(max_length=10, unique=True)
    dob = models.DateField(blank=True, null=True)
    sex = models.CharField(
        max_length=6,
        choices=SEX_CHOICES,
        blank=True,
        null=True
    )
    description = models.CharField(max_length=500)
    employer = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )
    website_url = models.URLField()
    twitter_url = models.URLField()
    facebook_url = models.URLField()
    user_skills = models.ManyToManyField(UserSkill, blank=True)

    def __unicode__(self):
        return self.phone


class EventifyUser(models.Model):
    auth_user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    firebase_id = models.CharField(max_length=200, unique=True)
    fcm_token = models.CharField(
        max_length=320, unique=False, blank=True, null=True)
    blocked = models.BooleanField(default=False)
    user_profile_information = models.OneToOneField(
        UserProfileInformation,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="profile_info"
    )
    relationships = models.ManyToManyField('self', through='Relationship',
                                           symmetrical=False,
                                           related_name='related_to')

    def __unicode__(self):
        try:
            return self.auth_user.first_name
        except AttributeError:
            return str(self.pk)

    def add_relationship(self, person, status, event):
        relationship, created = Relationship.objects.get_or_create(
            from_person=self,
            to_person=person,
            status=status,
            event=event)
        # if symm:
        #     # avoid recursion by passing `symm=False`
        #     person.add_relationship(self, status, event, False)
        return relationship

    def update_relationship(self, person, status):
        relationship = Relationship.objects.filter(
            from_person=person,
            to_person=self).update(status=status)
        print relationship
        # if symm:
        #     # avoid recursion by passing `symm=False`
        #     person.update_relationship(self, status, event, False)
        return relationship

    def remove_relationship(self, person, status, symm=True):
        Relationship.objects.filter(
            from_person=self,
            to_person=person,
            status=status).delete()
        # if symm:
        # avoid recursion by passing `symm=False`
        # person.remove_relationship(self, status, False)
        return

    def get_relationships(self, status):
        return self.relationships.filter(
            to_people__status=status,
            to_people__to_person=self)

    def get_pending_relationships(self):
        return self.relationships.filter(
            to_people__status=RELATIONSHIP_PENDING,
            to_people__to_person=self)

    def get_accepted_relationships(self):
        self.get_relationships(RELATIONSHIP_ACCEPTED)

    def get_blocked_relationships(self):
        self.get_relationships(RELATIONSHIP_BLOCKED)


class Panelist(models.Model):
    user = models.OneToOneField(
        EventifyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __unicode__(self):
        return self.user.auth_user.first_name + " " + self.user.auth_user.last_name


class Organiser(models.Model):
    user = models.OneToOneField(
        EventifyUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __unicode__(self):
        return self.user.auth_user.first_name + " " + self.user.auth_user.last_name


class EventCategory(models.Model):
    category_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.category_name


class Venue(models.Model):
    venue_name = models.CharField(max_length=50)
    venue_seat_capacity = models.IntegerField()
    location = PlacesField(blank=True, null=True)
    venue_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    venue_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True)
    venue_latitude_str = models.CharField(max_length=50, blank=True, null=True)
    venue_longitude_str = models.CharField(
        max_length=50, blank=True, null=True)

    def clean(self):
        self.venue_latitude_str = self.location.latitude
        self.venue_longitude_str = self.location.longitude

    def __unicode__(self):
        return self.venue_name


class Event(models.Model):
    event_bg_image = CloudinaryField('image', blank=True, null=True)
    event_category = models.ManyToManyField(EventCategory)
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE)
    agenda = models.TextField()
    event_name = models.CharField(max_length=50)
    event_start_time = models.DateTimeField()
    event_end_time = models.DateTimeField()
    entry_code = models.CharField(max_length=7)
    organiser = models.ManyToManyField(Organiser)
    panelist = models.ManyToManyField(Panelist)
    booking = models.ManyToManyField(EventifyUser, through='UserEventBooking')
    feedback = models.ManyToManyField(
        EventifyUser, related_name="event_user_feedback", through='UserEventFeedback')
    qr_code_url = models.URLField(blank=True, null=True)
    closed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.event_name


class EventTalk(models.Model):
    event = models.ForeignKey(
        Event, related_name='talks', on_delete=models.CASCADE, blank=True, null=True)
    talk_name = models.CharField(max_length=100)
    talk_description = models.TextField(blank=True, null=True)
    talk_start_time = models.TimeField(
        default=datetime.now, blank=True, null=True)
    talk_end_time = models.TimeField(
        default=datetime.now, blank=True, null=True)
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
    file = models.FileField(upload_to="documents", blank=True, null=True)
    attachment_url = models.URLField(blank=True, null=True)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    event_talk = models.ForeignKey(
        EventTalk, on_delete=models.CASCADE, related_name='talks_attachments', blank=True, null=True)

    def __unicode__(self):
        return self.file.path


class UserEventBooking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(EventifyUser, on_delete=models.CASCADE)
    booking_datetime = models.DateTimeField(default=datetime.now, blank=True)
    booking_seat_count = models.IntegerField(default=1)
    pin_verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.event.event_name + " - " + self.user.firebase_id

    class Meta:
        unique_together = ('event', 'user',)


# False - negative response, True - Positive response
# In case of rating < 3, True for boolean will mean that
# the user didn't like the respective boolean field
# In case of rating > 3, True for boolean will mean that
# the user liked the respective boolean field
class UserEventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(EventifyUser, on_delete=models.CASCADE)
    rating = IntegerRangeField(min_value=1, max_value=5, blank=True, null=True)
    feedback_text = models.CharField(max_length=500, blank=True, null=True)
    food = models.BooleanField(default=False)
    panelist = models.BooleanField(default=False)
    relevance = models.BooleanField(default=False)
    engagement = models.BooleanField(default=False)
    duration = models.BooleanField(default=False)
    crowd = models.BooleanField(default=False)

    def __unicode__(self):
        return self.event.event_name + " - " + self.user.firebase_id


class Question(models.Model):
    by_user = models.ForeignKey(EventifyUser, on_delete=models.CASCADE)
    event_talk = models.ForeignKey(
        EventTalk, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=250)
    answer_text = models.CharField(max_length=250)

    def __unicode__(self):
        return self.event.question_text


class EventCoupon(models.Model):
    event = models.ForeignKey(
        Event, related_name='coupons', on_delete=models.CASCADE, blank=True, null=True)
    provider_name = models.CharField(max_length=250, blank=True, null=True)
    coupon_description = models.CharField(
        max_length=250, blank=True, null=True)
    coupon_url = models.URLField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return self.coupon_description


class Relationship(models.Model):
    from_person = models.ForeignKey(
        EventifyUser, related_name='from_people', on_delete=models.CASCADE)
    to_person = models.ForeignKey(
        EventifyUser, related_name='to_people', on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, related_name='met_at_event', on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(
        choices=RELATIONSHIP_STATUSES, default=RELATIONSHIP_PENDING)
    sent_time = models.DateTimeField(default=timezone.now)
    response_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        try:
            return self.from_person.firebase_id + " -> " + self.to_person.firebase_id
        except AttributeError:
            return str(self.pk)
