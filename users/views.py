from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
