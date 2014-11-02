from rest_framework import serializers
from django.core.exceptions import ValidationError
import server.models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Course
        fields = ('id', 'name', 'start_date', 'end_date')

class MinimalCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Course
        fields = ('id', 'name')     

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.University
        fields = ('id', 'name','latitude', 'longitude',)

class ActiveCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Course
        fields = ('id',)        

class StudentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True)
    active_courses = ActiveCourseSerializer(many=True)
    university = UniversitySerializer(many=False)
    # learning_style = serializers.CharField(source='get_style_display')
    # level_of_study = serializers.CharField(source='get_level_display')
    # year_of_study = serializers.CharField(source='get_year_display')     
    class Meta:
        model = server.models.Student
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'courses', 'active_courses', 'university', 'year_of_study', 'program', 'learning_style', 'level_of_study', 'about_me')        

class MinimalStudentSerializer(serializers.ModelSerializer):
    learning_style = serializers.CharField(source='get_style_display')
    level_of_study = serializers.CharField(source='get_level_display')
    year_of_study = serializers.CharField(source='get_year_display')    
    class Meta:
        model = server.models.Student
        fields = ('id', 'username', 'first_name', 'year_of_study', 'program', 'learning_style', 'level_of_study', 'about_me')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Location
        fields = ('id', 'latitude', 'longitude', 'name', 'university', 'frequency')

class onCampusSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.onCampusSession
        fields = ('id', 'coordinator', 'course', 'location', 'attendees', 'start_time', 'end_time', 'room_number', 'max_participants', 'description')

class offCampusSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.offCampusSession
        fields = ('id', 'coordinator', 'course', 'latitude', 'longitude', 'attendees', 'start_time', 'end_time', 'name', 'max_participants', 'description')        

class SessionViewSerializer(onCampusSessionSerializer):
    course = MinimalCourseSerializer(many=False)
    coordinator = MinimalStudentSerializer(many=False)
    location = LocationSerializer(many=False)
    attendees = MinimalStudentSerializer(many=True)

class offCampusSessionViewSerializer(offCampusSessionSerializer):
    course = MinimalCourseSerializer(many=False)
    coordinator = MinimalStudentSerializer(many=False)
    attendees = MinimalStudentSerializer(many=True)    

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Student
        fields = ('id', 'username', 'password', 'email')

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(serializers.ModelSerializer, self).__init__(*args, **kwargs)

        if fields:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate(self, attrs):
        """
        Ensure username and email don't already exist in the database
        """
        print attrs
        if 'username' in attrs and server.models.Student.objects.filter(username=attrs['username']).exists():
            raise ValidationError("username")
        elif 'email' in attrs and server.models.Student.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("email")
        else:
            return attrs

