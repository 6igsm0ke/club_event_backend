from django.db import models
# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class ClubRelated(models.Model):
    club = models.ForeignKey(Club, verbose_name="Club related", on_delete=models.CASCADE)
    user = models.ForeignKey("users.CustomUser", verbose_name="User", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["club", "user"]


class ClubEvent(models.Model):
    club = models.ForeignKey(Club, verbose_name="Club related", on_delete=models.CASCADE)
    event = models.ForeignKey("events.Event", verbose_name="Event related", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["club", "event"]