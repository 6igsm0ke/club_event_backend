from rest_framework import serializers
from .models import Event


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
            "organizer",
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["organizer"] = instance.organizer.username