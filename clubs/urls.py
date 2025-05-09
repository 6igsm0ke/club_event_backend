from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ClubViewSet, ClubEventViewSet

router = DefaultRouter()
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'club_events', ClubEventViewSet, basename='clubevent')

urlpatterns = router.urls

urlpatterns += []