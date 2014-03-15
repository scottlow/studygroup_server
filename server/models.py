from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# @receiver(post_save, sender=get_user_model())
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

class University(models.Model):
    name = models.CharField(max_length=100);

class Course(models.Model):
    university = models.ForeignKey(University)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name    

class Student(AbstractUser):
    courses = models.ManyToManyField(Course)  

@receiver(post_save, sender=Student)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)    

class Location(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()
	name = models.CharField(max_length=100)
	room_number = models.IntegerField(null=True)
	university = models.ForeignKey(University)
	frequency = models.IntegerField()

class Session(models.Model):
	coordinator = models.ForeignKey(Student, related_name="session_coordinator")
	course = models.ForeignKey(Course)
	latitude = models.FloatField()
	longitude = models.FloatField()
	location = models.ForeignKey(Location)
	attendees = models.ManyToManyField(Student, related_name="session_attendees")
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()