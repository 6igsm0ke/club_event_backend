from rest_framework import viewsets
from .models import Event
from .serializers import EventSerializer
from .permissions import IsClubOrReadOnly
from clubs.models import ClubEvent  # не забудь импортировать!
from users.models import CustomUser  # если нужно
from rest_framework.exceptions import PermissionDenied, ValidationError

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-date')
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
                raise ValidationError("Клуб не найден для пользователя.")
        else:
            raise PermissionDenied("Только клуб может создавать ивенты.")
