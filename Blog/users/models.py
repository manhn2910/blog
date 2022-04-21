from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='media', default='media/avatar_default.png/')
