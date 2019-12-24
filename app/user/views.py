from user.serializers import UserSerializer
from rest_framework import generics


class CreateUserView(generics.CreateAPIView):
    """Creates an user"""
    serializer_class = UserSerializer
