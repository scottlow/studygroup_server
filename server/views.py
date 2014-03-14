from rest_framework import viewsets
from server.serializers import StudentSerializer, CourseSerializer
from rest_framework import permissions
from server.models import Course, Student
from server.permissions import IsOwnerOrReadOnly

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = Student 

class AddCourseView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 

    def pre_save(self, obj):
        obj.owner = self.request.user   