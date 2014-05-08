from rest_framework import generics, status, viewsets, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from server.models import Course, Student, University, Session, Location, onCampusSession
from django.http import HttpResponse, HttpResponseServerError, Http404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import obtain_auth_token, Token
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

import server.serializers

import logging

logger = logging.getLogger(__name__)


class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)    
    queryset = Student.objects.all()
    serializer_class = server.serializers.StudentSerializer


class StudentProfileView(generics.RetrieveUpdateAPIView):
    """Retrieves or updates the current student's info given correct token.

    Retrieve returns as JSON:
    {
        "id": <id>,
        "username": <username>,
        "email": <email>,
        "first_name": <first_name>,
        "last_name": <last_name>,
        "courses": [<courses>],
        "university": <university>
    }
    """

    serializer_class = server.serializers.StudentSerializer
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return self.request.user


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

            for course in serializer.init_data["courses"]:
                course_to_add = None
                try:
                    course_to_add = Course.objects.get(pk=course["id"])
                except KeyError:
                    HttpResponseServerError("Malformed JSON data.")

                if course_to_add != None:
                    student.courses.add(course_to_add)
                    if(course["active"] == True):
                        student.active_courses.add(course_to_add)

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
            request.user.active_courses.add(course_to_add)            
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
            request.user.active_courses.remove(course_to_remove)            
            request.user.save() 
        else:
            HttpResponseServerError("Invalid course_id specified.")

        return HttpResponse("success")

class FilterCourseView(generics.CreateAPIView):
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

        course_to_filter = Course.objects.get(pk=course_id)

        if course_to_filter != None:
            if course_to_filter in request.user.active_courses.all():
                request.user.active_courses.remove(course_to_filter)
            else:
                request.user.active_courses.add(course_to_filter)           
            request.user.save() 
        else:
            HttpResponseServerError("Invalid course_id specified.")

        return HttpResponse("success")                  

class UniversityView(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)    
    queryset = University.objects.all()
    serializer_class = server.serializers.UniversitySerializer

class UniversityLocationsView(generics.ListAPIView):
    permission_classes = (AllowAny,)    
    serializer_class = server.serializers.LocationSerializer

    def get_queryset(self):
        uni_id = self.kwargs['universityID']
        return Location.objects.filter(university__pk=uni_id)    

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
    serializer_class = server.serializers.SessionViewSerializer

    def get_queryset(self):
        course_ids = self.request.GET.getlist('id')
        print course_ids
        return onCampusSession.objects.filter(course__in=course_ids)

class SessionByUniversityView(generics.ListAPIView):
    """
    GET
    Returns a list of sessions based on the university it belongs to. 
    """
    permission_classes = (AllowAny,)
    serializer_class = server.serializers.onCampusSessionSerializer

    def get_queryset(self):
        uni_id = self.kwargs['universityID']
        return onCampusSession.objects.filter(
            course__in=[e.id for e in Course.objects.filter(university__pk=uni_id)]
        )

class SessionHostingView(generics.ListAPIView):
    """
    GET
    Returns a list of sessions where the authenticated user is the coordinator. 
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = server.serializers.SessionViewSerializer

    def get_queryset(self):
        return onCampusSession.objects.filter(
            coordinator__pk=self.request.user.id)


class SessionCreateView(generics.CreateAPIView):
    """ Creates a new session.

    Given the IDs of coordinator, course_id, location, and the start & end
    times, creates a new session.
    """

    authentication_classes = (TokenAuthentication,)
    serializer_class = server.serializers.onCampusSessionSerializer

    def post(self, request, *args, **kwargs):
        if 'location' not in request.DATA:
            return Response("Location ID Missing.",
                            status=status.HTTP_400_BAD_REQUEST)

        location = Location.objects.get(pk=request.DATA['location'])
        print request.DATA
        serializer = self.get_serializer(data=request.DATA)

        if serializer.is_valid():
            location.frequency += 1
            location.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class SessionAttendingView(generics.ListAPIView):
    """
    GET
    Returns a list of sessions that the authenticated user is attending
    """
    authentication_classes = (TokenAuthentication,)
    serializer_class = server.serializers.SessionViewSerializer

    def get_queryset(self):
        return onCampusSession.objects.filter(attendees=self.request.user)


class SessionJoinView(generics.CreateAPIView):
    """
    POST
    Appends current user to the attendees of session with the given session ID.
    """
    authentication_classes = (TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        # Get the session with the session ID.
        try:
            session = onCampusSession.objects.get(pk=request.DATA['session_id'])
        except ObjectDoesNotExist:
            return Response("There is no session with that given ID.",
                            status=status.HTTP_400_BAD_REQUEST)

        # Append only when you are not the coordinator, and you are not
        # already attending that session.
        if session.coordinator.id == request.user.id:
            return Response("You are the coordinator of this session, "
                            "so there is no need to add yourself to the list "
                            "of attendees.",
                            status=status.HTTP_400_BAD_REQUEST)
        elif session.attendees.filter(id=request.user.id).exists():
            return Response("User {} is already attending this session.".
                            format(request.user.username),
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            session.attendees.add(request.user)
            return Response("User {} added to session with ID {}.".
                            format(request.user.username, session.id),
                            status=status.HTTP_200_OK)

class SessionUpdateView(mixins.UpdateModelMixin, GenericAPIView):
    """ PATCH. Updates a session given its ID in the database.

    Returns {"detail": "Not found"} if no session with that ID exists,
    and updates the session if it exists in the database.

    ** Did not use generics.UpdateAPIView because it seems silly to be able to
    create new sessions with PUT when we already have SessionCreateView for
    that.
    """

    authentication_classes = (TokenAuthentication,)
    serializer_class = server.serializers.onCampusSessionSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        if 'id' in self.request.DATA:
            session_id = self.request.DATA['id']
            try:
                return onCampusSession.objects.get(pk=session_id)
            except ObjectDoesNotExist:
                logger.debug("Tried to update Session with id {}, but could "
                             "not find it.".format(session_id))
        raise Http404
