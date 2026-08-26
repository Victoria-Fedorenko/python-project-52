from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView, UpdateView
from .forms import CustomUserCreationForm



class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = '/login/'  # Redirect to login page after successful registration


class UserUpdateView(UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = '/users/'  # Redirect to user list after successful update
