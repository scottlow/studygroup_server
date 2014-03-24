from rest_framework import serializers
from django.core.exceptions import ValidationError
import server.models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Course
        fields = ('id', 'university', 'name', 'start_date', 'end_date')
     
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Student
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'courses')

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.University
        fields = ('name','latitude', 'longitude',)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Location
        fields = ('id', 'latitude', 'longitude', 'name', 'university' ,'room_number', 'frequency')

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Session
        fields = ('id', 'coordinator', 'latitude', 'longitude', 'course', 'location', 'attendees', 'start_time', 'end_time')

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Student
        fields = ('id', 'username', 'password', 'email')

    def validate(self, attrs):
        """
        Ensure username and email don't already exist in the database
        """
        if server.models.Student.objects.filter(username=attrs['username']).exists():
            raise ValidationError("username")
        elif server.models.Student.objects.filter(email=attrs["email"]).exists():
            raise ValidationError("email")
        else:
            return attrs

