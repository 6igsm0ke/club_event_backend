from rest_framework import serializers
from .models import *    

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ["id", "name", "email"]
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"read_only": True},
        }

class ClubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubEvent
        fields = ['id', 'club', 'event']
        extra_kwargs = {
            'id': {'read_only': True},
        }
