from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

app_name = "users"
router = DefaultRouter()
router.register("users", UserViewSet, basename="users")

urlpatterns = router.urls

urlpatterns += [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="get_token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("verify/<token_id>/", EmailVerificationView.as_view(), name="verify"),
    path(
        "request_password_reset/",
        PasswordResetView.as_view(),
        name="request_password_reset",
    ),
    path(
        "request_password_reset/<uuid:token_id>/",
        PasswordResetView.as_view(),
        name="password_reset",
    ),
]
