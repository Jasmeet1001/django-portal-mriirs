from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

# Create your views here.
def forbidden_page(request):
    return render(request, 'login/forbidden.html')
    
def login_page(request):
    return render(request, 'login/login_home.html')

def reset_pass(request):
    return render(request, 'login/reset_pass.html')
