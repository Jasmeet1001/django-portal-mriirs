from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import Signup

# Create your views here.
def create_account(request):
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            usrname = email.split('@')[0].split('.')[0]
            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with that email already exists")
            else:
                temp_save = form.save(commit=False)
                temp_save.username = usrname
                temp_save.save() 
                messages.success(request, f" Account created for {usrname}")
                return redirect('login')
    else:
        form = Signup()

    return render(request, 'login/account_creation.html', {'form': form})

def login_page(request):
    return render(request, 'login/login_home.html')

def reset_pass(request):
    return render(request, 'login/reset_pass.html')
