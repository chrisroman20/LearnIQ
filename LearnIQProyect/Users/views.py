import datetime
import os
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.files.storage import FileSystemStorage

from .models import UserStyle

# Create your views here.

def validate_user(request, id):
    if request.user.id != id:
        messages.error(request, 'No tienes permisos para editar este usuario')
        return False
    return True
@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Home(View):
    template_name = 'Users/home.html'
    context = {}
    def get(self, request):
        try:
            styleLearning = UserStyle.objects.get(user=request.user)
        except UserStyle.DoesNotExist:
            styleLearning = None
            
        self.context = {
            "user": request.user,
            "styleLearning": styleLearning
        }
        return render(request,self.template_name, self.context)
    
    def post(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    

@method_decorator(login_required, name='dispatch')
class EditUser(View):
    template_name = "Users/editUser.html"
    context = {}

    def get(self, request, id):
        user = request.user
        
        if validate_user(request, id):
            self.context = {
                "user": request.user,
            }
            return render(request, self.template_name, self.context)
        else:
            return redirect('Users:UsersHome')
        
    def post(self, request, id):

        user = request.user
        if validate_user(request, id):
            UserModel = get_user_model()
            name = request.POST.get('first_name')
            lastName = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            image = request.FILES.get('image')

            if image:
                upload_dir = os.path.join('users', datetime.now().strftime('%Y/%m/%d'))
                fs = FileSystemStorage()
                filename = fs.save(upload_dir+'/'+ image.name, image)
                image_url =filename
            else:
                image_url = 'users/default-img.jpg'

            user = UserModel.objects.filter(id=id).update(first_name=name, email=email, last_name=lastName, phone=phone, image=image_url)

        return redirect('Users:UsersHome')
    

    