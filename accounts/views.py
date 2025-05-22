# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import (
    get_user_model,
    login as django_login,
    logout as django_logout,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import MyTokenObtainPairSerializer

User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    """POST /api/token/ → { access, refresh }"""

    serializer_class = MyTokenObtainPairSerializer


class RegisterView(APIView):
    """
    POST /api/register/
    { "username": "...", "password": "..." }
    → 201: { access, refresh, username }
    """

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"detail": "username & password required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "username taken"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
def session_login(request):
    """
    POST /api/session_login/
    { "access": "<jwt>" }
    → 200 sets a Django session cookie so @login_required will succeed.
    """
    token = request.data.get("access")
    if not token:
        return Response(
            {"detail": "access token required"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Validate JWT and fetch user
    validated = JWTAuthentication().get_validated_token(token)
    user = JWTAuthentication().get_user(validated)

    # Log them into a Django session
    django_login(request, user)
    return Response({"ok": True})


def index(request):
    """GET / → serve the SPA page."""
    return render(request, "index.html")


def do_logout(request):
    """GET or POST /logout/ → clear the Django session and redirect to index."""
    django_logout(request)
    return redirect("index")
