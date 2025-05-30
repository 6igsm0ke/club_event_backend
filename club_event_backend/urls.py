from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/chat/", include("chat.urls")),
    path("api/v1/auth/", include("users.urls")),
    path("api/v1/events/", include("events.urls")),
    path("api/v1/clubs/", include("clubs.urls")),
]

# Добавляем только если DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
