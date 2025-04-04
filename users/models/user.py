from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mentor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='mentees')
