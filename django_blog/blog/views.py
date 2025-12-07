from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import CustomeUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

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


# postlist view -shows list of objects

class PostListView(ListView):
    model =Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

# post detail view shows single obj

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# postcreate view creates new posts

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# postupdate view used to edit obj

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model =Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return super().test_func()
    
# post delete view

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return super().test_func()