from rest_framework import viewsets
from server.serializers import StudentSerializer, CourseSerializer
from rest_framework import permissions
from server.models import Course, Student
from rest_framework import generics
from django.http import HttpResponse

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        """
        This view will return a list of all the courses for
        a particular university id
        """
        uni_id = self.kwargs['universityID']
        return Course.objects.filter(university__pk=uni_id)    

class AddCourseView(generics.CreateAPIView):
    serializer_class = StudentSerializer

    def post(self, request, *args, **kwargs):
        print request.user.courses
        print request.DATA

        return HttpResponse(status=200)