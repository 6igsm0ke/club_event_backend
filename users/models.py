from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from .managers import UserManager
from core.models import BaseOwnedModel
from django.utils.translation import gettext as _
from clubs.models import Club

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True)
    @classmethod
    def get_student(cls):
        return cls.objects.get_or_create(name="Student", code="STD")[0]

    @classmethod
    def get_club(cls):
        return cls.objects.get_or_create(name="Club", code="CLB")[0]

    def __str__(self):
        return self.name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def is_club_admin(self):
        position_codes = Role.objects.filter(
            rolerelated__user=self,
        ).values_list("code", flat=True)
        return "CLB" in position_codes

    @property
    def get_club(self):
        if not self.is_club_admin:
            return None
        return Club.objects.filter(clubrelated__user=self).first()

class RoleRelated(models.Model):
    role = models.ForeignKey(
        Role, verbose_name=_("Role related"), on_delete=models.CASCADE
    )
    user = models.ForeignKey(CustomUser, verbose_name=_("User"), on_delete=models.CASCADE)

    class Meta:
        unique_together = ["role", "user"]

class Token(BaseOwnedModel):
    PURPOSE_CHOICES = (
        (0, ("Registration")),
        (1, ("Reset password")),
    )
    purpose = models.SmallIntegerField(("Purpose"), choices=PURPOSE_CHOICES)
    is_used = models.BooleanField(default=False)

    @property
    def is_valid(self):
        return not self.is_used and timezone.now() - self.created < timezone.timedelta(
            hours=1
        )

    @classmethod
    def check_and_get_token(cls, token, purpose):
        try:
            tkn = cls.objects.get(pk=token, purpose=purpose)
            return [tkn.is_valid, tkn]
        except cls.DoesNotExist:
            return [False, None]