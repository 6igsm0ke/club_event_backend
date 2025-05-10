from rest_framework import serializers
from .models import Event, EventType


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all())
    registered_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "description",
            "location",
            "date",
            "created_at",
            "type",
            "image",
            "registered_count",
            "max_members",
        ]

    def get_registered_count(self, obj):
        return obj.registered_users.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["type"] = EventTypeSerializer(instance.type).data
        return data
