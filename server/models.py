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
    FIRST_YEAR = 1
    SECOND_YEAR = 2
    THIRD_YEAR = 3
    FOURTH_YEAR = 4
    FIFTH_YEAR = 5
    SIXTH_YEAR = 6
    SEVENTH_YEAR = 7   
    YEARS_OF_STUDY = (
        (FIRST_YEAR, 'First Year'),
        (SECOND_YEAR, 'Second Year'),
        (THIRD_YEAR, 'Third Year'),
        (FOURTH_YEAR, 'Fourth Year'),
        (FIFTH_YEAR, 'Fifth Year'),
        (SIXTH_YEAR, 'Sixth Year'),
        (SEVENTH_YEAR, 'Seventh Year'),
    )

    OTHER = 'OT'    

    UNDERGRADUATE = 'UN'
    MASTERS = 'MA'
    PHD = 'PH'
    LEVELS_OF_STUDY = (
        (UNDERGRADUATE, 'Undergraduate'),
        (MASTERS, 'Masters'),
        (PHD, 'PHD'),
        (OTHER, 'Other'),
    )

    AUDITORY = 'AU'
    VISUAL = 'VI'
    KINESTHETIC = 'KI'
    LEARNING_STYLES = (
        (AUDITORY, 'Auditory'),
        (VISUAL, 'Visual'),
        (KINESTHETIC, 'Kinesthetic'),
        (OTHER, 'Other'),
    )

    year_of_study = models.IntegerField(choices=YEARS_OF_STUDY, default=FIRST_YEAR)
    level_of_study = models.CharField(max_length=2, choices=LEVELS_OF_STUDY, default=UNDERGRADUATE)
    learning_style = models.CharField(max_length=2, choices=LEARNING_STYLES, default=AUDITORY) 
    program = models.CharField(max_length=50)
    about_me = models.CharField(max_length=400)    

    courses = models.ManyToManyField(Course, related_name="courses")
    active_courses = models.ManyToManyField(Course, related_name="active_courses")
    university = models.ForeignKey(University, related_name="university")

    def get_year_display(self):
        for year in self.YEARS_OF_STUDY:
            if year[0] == self.year_of_study:
                return year[1]

    def get_level_display(self):
        for level in self.LEVELS_OF_STUDY:
            if level[0] == self.level_of_study:
                return level[1]

    def get_style_display(self):
        for style in self.LEARNING_STYLES:
            if style[0] == self.learning_style:
                return style[1]                                    

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
    # Null=True and blank=True to allow sessions to have no coordinators
    # should they choose to leave the session that they're coordinating
    coordinator = models.ForeignKey(Student, related_name="%(app_label)s_%(class)s_related_coordinator", null=True, blank=True)
    course = models.ForeignKey(Course)
    attendees = models.ManyToManyField(Student, related_name="%(app_label)s_%(class)s_related_attendees")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.CharField(max_length=400)
    max_participants = models.IntegerField()

    class Meta:
        abstract = True

class onCampusSession(Session):
    location = models.ForeignKey(Location)
    room_number = models.IntegerField(null=True)  
    
class offCampusSession(Session):
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=100) 
    address_string = models.CharField(max_length=150)