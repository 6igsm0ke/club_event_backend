from django.db import models
from django.contrib.auth import get_user_model

class EventType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    bonus = models.CharField(max_length=100, blank=True, null=True)
    max_members = models.PositiveIntegerField(default=100)
    
    registered_users = models.ManyToManyField(User, related_name='registered_events', blank=True)
    clubs = models.ManyToManyField('clubs.Club', through='clubs.ClubEvent', related_name='events')

    def __str__(self):
        return self.title

    @property
    def registered_count(self):
        return self.registered_users.count()

    @property
    def club(self):
        return self.clubs.first()