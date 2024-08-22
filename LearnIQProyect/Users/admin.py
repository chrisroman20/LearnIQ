from django.contrib import admin
from .models import User
from .models import UserStyle

# Register your models here.
admin.site.register(User)
admin.site.register(UserStyle)
