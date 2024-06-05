from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

@method_decorator(login_required(login_url='/login/'), name='dispatch')
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