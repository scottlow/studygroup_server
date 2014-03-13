from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from server.serializers import UserSerializer
from rest_framework import permissions

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  