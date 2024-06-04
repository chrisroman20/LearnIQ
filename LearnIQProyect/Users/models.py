from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    UserRol = models.CharField(max_length=50, blank=True, null=False, default='user')

    def getImage(self):
        if self.image:
            return self.image.url
        return 'users/default-img.jpg'