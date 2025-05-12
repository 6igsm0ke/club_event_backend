from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer
from .permissions import IsClubOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from clubs.models import ClubEvent
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.response import Response
from users.utils import send_event_registration_email


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer
    permission_classes = [IsClubOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_club_admin:
            club = user.get_club
            if club:
                event = serializer.save()
                ClubEvent.objects.create(club=club, event=event)
            else:
                raise ValidationError("Club not found.")
        else:
            raise PermissionDenied("Only club admins can create events.")

    def perform_update(self, serializer):
        user = self.request.user
        if not user.is_club_admin:
            raise PermissionDenied("Only club admins can update events.")

        event = serializer.save()


class RegisterToEventView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise NotFound("Event not found.")

        user = request.user

        if user in event.registered_users.all():
            raise ValidationError("You already registered for this event.")

        if (
            event.max_members is not None
            and event.registered_users.count() >= event.max_members
        ):
            raise ValidationError("Maximum number of participants reached.")
        send_event_registration_email(user, event)
        event.registered_users.add(user)
        return Response(
            {"message": "You registered succesdfully!"}, status=status.HTTP_200_OK
        )


class EventTypesViewSet(viewsets.ModelViewSet):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset.order_by("name")
