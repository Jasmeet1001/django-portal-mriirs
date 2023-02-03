"""ric_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from login import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('register/', user_views.create_account, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login/login_home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login/logout_home.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='login/reset_pass.html'), name = 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='login/reset_pass_done.html'), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='login/reset_pass_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='login/reset_pass_complete.html'), name = 'password_reset_complete'),
    path('', include('dashboard.urls')),
]
