from rest_framework import serializers
from .models import Event, EventType

class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = ["id", "name"]

class EventSerializer(serializers.ModelSerializer):
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
        ]
        def to_representation(self, instance):
            data = super().to_representation(instance)
            data["type"] = EventTypeSerializer(instance.type).data
            return data