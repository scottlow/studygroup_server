from rest_framework import viewsets
from server.serializers import StudentSerializer, CourseSerializer
from rest_framework import permissions
from server.models import Course, Student
from rest_framework import generics

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AddCourseView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = StudentSerializer