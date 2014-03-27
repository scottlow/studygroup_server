from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from server.models import Course, Student, University, Session
from django.http import HttpResponse, HttpResponseServerError
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import obtain_auth_token, Token
from django.core.exceptions import ValidationError

import server.serializers


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)    
    queryset = Student.objects.all()
    serializer_class = server.serializers.StudentSerializer

class StudentProfileView(generics.ListAPIView):
    """
    A view that will return a student's information given the correct
    authentication token
    Returns as JSON:
    {
        "id": <id>,
        "username": <username>,
        "email": <email>,
        "first_name": <first_name>,
        "last_name": <last_name>,
        "courses": []
    }
    """
    serializer_class = server.serializers.StudentSerializer
    authentication_classes = (TokenAuthentication,)
    def get_queryset(self):
        return Student.objects.filter(pk=self.request.user.id)

class CourseList(generics.ListAPIView):
    """
    This view will return a list of all the courses for
    a particular university id
    """         
    serializer_class = server.serializers.CourseSerializer
    permission_classes = (AllowAny,)

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
        serializer = server.serializers.StudentRegisterSerializer(data=request.DATA)
        if serializer.is_valid():
            student = Student.objects.create_user(
                username=serializer.init_data["username"],
                password=serializer.init_data["password"],
                email=serializer.init_data["email"],
                university=University.objects.get(id=serializer.init_data['university']),
            )
            student.first_name = serializer.init_data['name']          
            student.save()
            token, created = Token.objects.get_or_create(user=student)
            return Response(data={'token':token.key}, status=200)
        else:
            header = {"Access-Control-Expose-Headers": "Error-Message, Error-Type"}
            errors = serializer.errors["non_field_errors"]
            if errors:
                if errors[0] == "username":
                    header["Error-Type"] = errors[0]
                    header["Error-Message"] = "Username {0} already exists".format(serializer.init_data['username'])                  
                elif errors[0] == "email":
                    header['Error-Type'] = errors[0]
                    header["Error-Message"] = "Email {0} already exists".format(serializer.init_data['email'])
            return Response(headers=header, status=400)

class AddCourseView(generics.CreateAPIView):
    """
    This view provides an endpoint for users to
    add courses to their courses list.
    """        
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        course_id = None
        try:
            course_id = request.DATA['course_id']
        except KeyError:
            HttpResponseServerError("Malformed JSON data.")

        course_to_add = Course.objects.get(pk=course_id)

        if course_to_add != None:
            request.user.courses.add(course_to_add)
            request.user.save()  
        else:
            HttpResponseServerError("Invalid course_id specified.")

        return HttpResponse("success")

class RemoveCourseView(generics.CreateAPIView):
    """
    This view provides an endpoint for users to
    remove a course from their courses list.
    """        
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        course_id = None
        try:
            course_id = request.DATA['course_id']
        except KeyError:
            HttpResponseServerError("Malformed JSON data.")

        course_to_remove = Course.objects.get(pk=course_id)

        if course_to_remove != None:
            request.user.courses.remove(course_to_remove)
            request.user.save() 
        else:
            HttpResponseServerError("Invalid course_id specified.")

        return HttpResponse("success")        

class UniversityView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)    
    queryset = University.objects.all()
    serializer_class = server.serializers.UniversitySerializer

class SessionPerCourseView(generics.ListAPIView):
    """
    GET
    Returns a session based on the course id or course ids
    provided. Input is expected as
    id=1&id=2
    or
    id=1
    Here is a full url endpoint with get parameters
    /sessions/courses/id=1&id=2
    Returns:
    A session model object in JSON
    """

    permission_classes = (AllowAny,)
    serializer_class = server.serializers.SessionSerializer

    def get_queryset(self):
        course_ids = self.request.GET.getlist('id')
        print course_ids
        return Session.objects.filter(course__in=course_ids)