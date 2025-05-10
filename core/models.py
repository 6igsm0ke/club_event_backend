import json
import logging
from uuid import uuid4
from django.db import models
from django.utils.translation import gettext as _
from django.core.cache import cache
from django.core.serializers import serialize
from django.http import HttpRequest
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    uuid = models.UUIDField(
        ("Unique identifier"),
        primary_key=True,
        default=uuid4,
        unique=True,
        editable=False,
    )
    is_active = models.BooleanField(_("Active"), default=True)
    created = models.DateTimeField(
        ("Created"),
        auto_now_add=True,
    )
    updated = models.DateTimeField(("Updated"), auto_now=True)

    class Meta:
        abstract = True

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    def __str__(self):
        if hasattr(self, "name") and len(self.name) > 0:
            return self.name
        elif hasattr(self, "name_en_us") and self.name_en_us is not None:
            return self.name_en_us
        elif hasattr(self, "name_kk") and self.name_kk is not None:
            return self.name_kk
        elif hasattr(self, "name_ru") and self.name_ru is not None:
            return self.name_ru
        else:
            return super(BaseModel, self).__str__()

    def save(self, *args, **kwargs):
        super(BaseModel, self).save(*args, **kwargs)
        data = json.loads(
            serialize(
                "json",
                [
                    self,
                ],
            )
        )[0]
        if hasattr(HttpRequest, "user") and hasattr(HttpRequest.user, "uuid"):
            user = HttpRequest.user
        else:
            user = None  # danger

        prev_data = ActionHistory.objects.filter(recording_uuid=data.get("pk"))
        try:
            if prev_data.exists():
                last_data = prev_data.order_by("created").last().new_data
                action = ActionHistory.objects.create(
                    recording_uuid=data.get("pk"),
                    model=data.get("model"),
                    author=user,
                    action_type=1,
                    new_data=data,
                    previous_data=last_data,
                )
            else:
                action = ActionHistory.objects.create(
                    recording_uuid=data.get("pk"),
                    model=data.get("model"),
                    action_type=0,
                    author=user,
                    new_data=data,
                )
            logging.info(action)
        except Exception as e:
            logging.error(e)

    def delete(self, *args, **kwargs):
        data = json.loads(
            serialize(
                "json",
                [
                    self,
                ],
            )
        )[0]
        try:
            user = HttpRequest.user
        except AttributeError:
            user = None
        try:
            action = ActionHistory.objects.create(
                recording_uuid=data.get("pk"),
                model=data.get("model"),
                author=user,
                action_type=2,
                previous_data=data,
            )
            logging.info(action)
        except ValueError:
            logging.error(ValueError)
        super(BaseModel, self).delete(*args, **kwargs)


class BaseCatalog(BaseModel):
    name = models.CharField(
        ("Name"),
        max_length=1000,
    )
    code = models.CharField(("Code"), max_length=100, blank=True, null=True, unique=True)

    class Meta:
        abstract = True
        ordering = [
            "name",
        ]


class ActionHistory(models.Model):
    ACTION_TYPE = (
        (0, ("Create")),
        (1, ("Modify")),
        (2, ("Delete")),
    )
    uuid = models.UUIDField(
        ("Unique identifier"),
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    created = models.DateTimeField(
        ("Created"),
        auto_now_add=True,
    )
    action_type = models.IntegerField(("Action type"), choices=ACTION_TYPE, default=0)
    recording_uuid = models.UUIDField(
        ("Record to apply"),
        default=uuid4,
        db_index=True,
    )
    model = models.CharField(
        ("Where stored"),
        default="",
        max_length=1000,
    )
    author = models.ForeignKey(
        "users.CustomUser",
        verbose_name=("Author of action"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    previous_data = models.JSONField(("Previous data"), null=True)
    new_data = models.JSONField(("New data"), null=True)

    class Meta:
        verbose_name = "Action history"
        verbose_name_plural = "Actions history"

    def __str__(self):
        try:
            return f"{self.get_action_type_display()} at {self.created} by {self.author.username}"
        except AttributeError:
            return f"{self.get_action_type_display()} at {self.created} by unknown"


class BaseOwnedModel(BaseModel):
    user = models.ForeignKey(
        "users.CustomUser",
        verbose_name=("owner of object"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class BaseMultiOwnedModel(BaseModel):
    users = models.ManyToManyField("users.User", blank=True)

    class Meta:
        abstract = True

class DynamicModelConfig(BaseModel):
    app_label = models.CharField(max_length=128)
    model_name = models.CharField(max_length=128)
    verbose_name = models.CharField(max_length=128)
    # filter_fields = models.JSONField(blank=True, default=list)

    def __str__(self):
        return f"{self.app_label}.{self.model_name}"
