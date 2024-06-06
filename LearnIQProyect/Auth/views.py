from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

class Home(View):
    template_name = 'Auth/home.html'
    context = {}
    def get(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    
    def post(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)


class Signup(View):
    template_name = "Auth/signup.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Crear un nuevo usuario
        UserModel = get_user_model()
        username = request.POST['userName']
        name = request.POST['Name']
        lastName = request.POST['LastName']
        email = request.POST['Mail']
        phone = request.POST['Phone']
        password = request.POST['Password']
        password2 = request.POST['confirmPassword']
        isAdmin = False
        if 'userRole' in request.POST:
            isAdmin = True
        image = request.FILES.get('image')
        if image == None:
            image = 'users/default-img.jpg'
        if password != password2:
            messages.error(request, 'The passwords do not match.')
            return render(request, self.template_name)
        if isAdmin:
            rol = 'admin'
        else:
            rol = 'user'
        if UserModel.objects.filter(email=email).exists() or UserModel.objects.filter(username=username).exists():
            messages.error(request, 'The email or username is already in use.\nPlease use another one.')
            return render(request, self.template_name)
        user = UserModel.objects.create_user(username=username, email=email, password=password, UserRol =rol,first_name=name,last_name=lastName,phone=phone,image=image)
        login(request, user)
        return redirect('App:AppHome')
        

class LogIn(View):
    template_name = "Auth/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
            user_mail = request.POST['userMail']
            user_password = request.POST['userPassword']

            user = authenticate(request, username=user_mail, password=user_password)
            if user is not None:
                login(request, user)
                return redirect('App:AppHome')
            else:
                messages.error(request, 'The email or password is incorrect.')
                return render(request, self.template_name)

@login_required 
def logout_view(request):
    logout(request)
    return redirect('HomePage')  # Redirigir a la página principal después de cerrar sesión

    
class ResetPassword(View):
    template_name = "Auth/resetPassword.html"
    context = {}

    def get(self, request):
        self.context = {
            "username": "RESET PASSWORD",
        }
        return render(request, self.template_name, self.context)
