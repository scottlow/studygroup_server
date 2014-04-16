from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class University(models.Model):
    name = models.CharField(max_length=100);
    latitude = models.FloatField()
    longitude = models.FloatField()

class Course(models.Model):
    university = models.ForeignKey(University)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name    

class Student(AbstractUser):
    courses = models.ManyToManyField(Course, related_name="courses")
    active_courses = models.ManyToManyField(Course, related_name="active_courses")
    university = models.ForeignKey(University, related_name="university") 

@receiver(post_save, sender=Student)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)    

class Location(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()
	name = models.CharField(max_length=100)
	university = models.ForeignKey(University)
	frequency = models.IntegerField()

class Session(models.Model):
	coordinator = models.ForeignKey(Student, related_name="session_coordinator")
	course = models.ForeignKey(Course)
	attendees = models.ManyToManyField(Student, related_name="session_attendees")
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()

	class Meta:
		abstract = True

class onCampusSession(Session):
    location = models.ForeignKey(Location)
    room_number = models.IntegerField(null=True)  
    
# class offCampusSession(Session):
#     location = models.ForeignKey(Location)

# I have a feeling that off campus sessions shouldn't even have locations. They should
# have a lat, long, and optional address (Street number, street name, etc) and we
# shouldn't really be keeping track of off campus locations in the database by id. 