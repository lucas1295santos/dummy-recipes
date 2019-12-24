from user.serializers import UserSerializer, UserAuthSerializer
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Creates an user"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new Auth token for an user"""
    serializer_class = UserAuthSerializer
    render_classes = api_settings.DEFAULT_RENDERER_CLASSES
