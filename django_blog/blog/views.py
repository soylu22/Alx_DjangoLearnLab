from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import CustomeUserCreationForm

# Create your views here.

# for the registration

def register_view(request):
    if request.method == 'POST':
        form = CustomeUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now login")
            return redirect('login')
        else:
            form = CustomeUserCreationForm()
        return render(request, 'blog/register.html', {'form': form})
    
# for login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'blog/login.html')

# for logout view

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')

# profile view

def profile_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.user.email = email
        request.user.save()
        messages.success(request, "Profile updated successfully!")
    return render(request, 'blog/profile.html')