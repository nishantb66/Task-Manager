# accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    index,
    RegisterView,
    MyTokenObtainPairView,
    session_login,
    do_logout,
)

urlpatterns = [
    path("", index, name="index"),
    path("logout/", do_logout, name="logout"),
    path("api/register/", RegisterView.as_view(), name="api_register"),
    path("api/token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/session_login/", session_login, name="session_login"),
]
