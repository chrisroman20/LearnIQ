from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=10, blank=True, null=True)
    image = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    UserRol = models.CharField(max_length=50, blank=True, null=False, default='user')

    def getImage(self):
        if self.image:
            return self.image.url
        return 'users/default-img.jpg'
    


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idToken = models.AutoField(primary_key=True)
    token = models.CharField(max_length=100, default='', blank=True)
    tipoToken = models.CharField(max_length=50, default='EMAIL', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = generateToken()
        super().save(*args, **kwargs)


def generateToken():
    while True:
        tokenGenerado = uuid.uuid4().hex
        if not Token.objects.filter(token=tokenGenerado).exists():
            return tokenGenerado