from rest_framework import serializers
import server.models

class CourseSerializer(serializers.Serializer):
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
        fields = ('name',)

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Location
        fields = ('id', 'latitude', 'longitude', 'name', 'university' ,'room_number', 'frequency')

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = server.models.Session
        fields = ('id', 'coordinator', 'latitude', 'longitude', 'course', 'location', 'attendees', 'start_time', 'end_time')

