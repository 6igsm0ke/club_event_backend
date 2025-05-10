from rest_framework import viewsets
from .permissions import ClubEventPermission
from .serializers import ClubSerializer, ClubEventSerializer
from .models import Club, ClubEvent
from django.shortcuts import render


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    permission_classes = [ClubEventPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Club.objects.filter(clubrelated__user=user)
        return Club.objects.none()


# Create your views here.
class ClubEventViewSet(viewsets.ModelViewSet):
    queryset = ClubEvent.objects.all()
    serializer_class = ClubEventSerializer
    permission_classes = [ClubEventPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ClubEvent.objects.filter(club__clubrelated__user=user)
        return ClubEvent.objects.none()

