import os
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from email.mime.text import MIMEText



import smtplib


from Users.models import Token
# Create your views here.

class Home(View):
    template_name = 'App/appHome.html'
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
    return redirect('HomePage')  
    
class ResetPassword(View):
    template_name = "Auth/resetPassword.html"
    context = {}

    def get(self, request):
        self.context = {
        }
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        email = request.POST['email']
        
        UserModel = get_user_model()
        if UserModel.objects.filter(email=email).exists():
            user = UserModel.objects.get(email=email)
            if SendEmail(email, user):
                messages.success(request, 'An email has been sent to reset your password.')
            else:
                messages.error(request, 'An error occurred while sending the email.')
            return redirect('Auth:signIn')
        else:
            messages.error(request, 'The email is not registered.')
        return render(request, self.template_name, self.context)
    
    
class ChangePassword(View):
    template_name = "Auth/changePassword.html"
    context = {}

    def get(self, request,token):
        self.context = {
        }

        IsValidToken = Token.objects.filter(token=token).exists()

        if IsValidToken:
            ObjToken = Token.objects.get(token=token)
            if ObjToken.status:
                messages.error(request, 'The token has already been used.')
                return redirect('Auth:resetPassword')
            return render(request, self.template_name, self.context)
        else:
            messages.error(request, 'The token is invalid.')
            return redirect('Auth:resetPassword')
    
    def post(self,request,token):
        password = request.POST['userPassword']
        password2 = request.POST['userPassword1']
        if password != password2:
            messages.error(request, 'The passwords do not match.')
            return render(request, self.template_name, self.context)
        IsValidToken = Token.objects.filter(token=token).exists()
        if IsValidToken:
            ObjToken = Token.objects.get(token=token)   
            if ObjToken.status and ObjToken.tipoToken == 'EMAIL':
                messages.error(request, 'The token has already been used.')
                return redirect('Auth:resetPassword')
            user = ObjToken.user
            user.set_password(password)
            user.save()
            ObjToken.status = True
            ObjToken.save()
            messages.success(request, 'The password has been changed successfully.')
            return redirect('Auth:signIn')
            
            
        return render(request, self.template_name, self.context)



def SendEmail(email,User):
    try:
        linkApp = 'http://127.0.0.1:8000/'
        linkRP = 'Auth/resetpassword/'
        gmail_user = 'angel.valrz@gmail.com'
        gmail_password = 'ljsynxrvshpdswgg'
        subject = 'Password recovery - LearnIQ'
        to = [email]

        token = Token.objects.create(user=User)
        token.save()
        reset_link = f'{linkApp}{linkRP}{token.token}'

        emailTemplate = """<!DOCTYPE html>
                                <html>
                                <head>
                                </head>
                                <body style='font-family: Arial, sans-serif;background-color: #f5f5f5; margin: 0;padding: 0;height: 100vh;display: flex;justify-content: center;align-items: center;'>
                                    <div style=' background-color: #ffffff;max-width: 600px;padding: 20px;border: 1px solid #ccc;border-radius: 5px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);text-align: center;'>
                                        <a href="{linkApp}" class="navbar-brand d-flex align-items-center">
                                            <h2 class="text-primary text-sm-start">LearnIQ</h2>
                                        </a>
                                        <h1 style="color: #333;">Password recovery request</h1>
                                        <p>Hi! {User.name} {User.LastName}, you have requested to recover your password.</p>
                                        <p><strong>This is the link to change the password:</strong></p>
                                        <p style='font-size: 24px; font-weight: bold;'>{resetLink}</p>
                                        <p stye='color: #666;font-size: 16px;'>Please change your password immediately after logging in.</p>
                                    </div>
                                </body>
                                </html>"""
        emailTemplate = emailTemplate.replace('{User.name}', User.first_name)
        emailTemplate = emailTemplate.replace('{User.LastName}', User.last_name)
        emailTemplate = emailTemplate.replace('{resetLink}', reset_link)
        emailTemplate = emailTemplate.replace('{linkApp}', linkApp)



        msg = MIMEText(emailTemplate, 'html')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = ', '.join(to)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to, msg.as_string())
        server.close()
        print   ('Connection successful')
        return True
    except Exception as e:
        print('Something went wrong... ',e)
        return False
    