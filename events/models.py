from django.db import models

class EventType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    clubs = models.ManyToManyField('clubs.Club', through='clubs.ClubEvent', related_name='events')


    def __str__(self):
        return self.title
