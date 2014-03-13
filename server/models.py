from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class University(models.Model):
	name = models.CharField(max_length=100);

class Course(models.Model):
	university = models.ForeignKey(University);
	name = models.CharField(max_length=100)
	start_date = models.DateField();
	end_date = models.DateField();
