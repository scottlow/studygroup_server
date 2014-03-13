from django.contrib.auth.models import User
from rest_framework import viewsets
from server.serializers import UserSerializer, CourseSerializer
from rest_framework import permissions
from server.models import Course

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 