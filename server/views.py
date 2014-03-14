from rest_framework import viewsets, permissions, generics
from server.serializers import StudentSerializer, CourseSerializer
from server.models import Course, Student
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CourseList(generics.ListAPIView):
    """
    This view will return a list of all the courses for
    a particular university id
    """         
    serializer_class = CourseSerializer

    def get_queryset(self):
        uni_id = self.kwargs['universityID']
        return Course.objects.filter(university__pk=uni_id) 

class RegisterUserView(generics.CreateAPIView):  
    """
    This view provides an endpoint for new users
    to register.
    """    
    permission_classes = (AllowAny,)    
    def post(self, request, *args, **kwargs):
        print request.DATA

        return HttpResponse(status=200)

class AddCourseView(generics.CreateAPIView):
    """
    This view provides an endpoint for users to
    add courses to their courses list.
    """        
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        # json_data = simplejson.loads(request.DATA)
        # try:
        #     course_id = json_data['course_id']
        # except KeyError:
        #     HttpResponseServerError("Malformed JSON data.")
        print request.DATA

        return HttpResponse("success")