from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model inheriting from Django's AbstractUser.
    This gives us all the fields of a standard User (username, password, email, etc.)
    and we can add our custom fields on top.
    """
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    tokens = models.IntegerField(default=4000)

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    