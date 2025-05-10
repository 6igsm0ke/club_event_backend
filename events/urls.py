from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import EventViewSet, RegisterToEventView, EventTypesViewSet

router = DefaultRouter()
router.register(r"events", EventViewSet, basename="event")

urlpatterns = router.urls

urlpatterns += [path("register/<int:event_id>/", RegisterToEventView.as_view(), name="event-register"),
                path("types/", EventTypesViewSet.as_view({"get": "list"}), name="event-types")]
