from rest_framework import viewsets, permissions, generics
from server.serializers import StudentSerializer, CourseSerializer
from server.models import Course, Student
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

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

class RegisterUserView(generics.CreateAPIView):  
    permission_classes = (AllowAny,)    
    def post(self, request, *args, **kwargs):
        print request.DATA

        return HttpResponse(status=200)

class AddCourseView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        print request.user.username
        print request.DATA

        return HttpResponse(status=200)