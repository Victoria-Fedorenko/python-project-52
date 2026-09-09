from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()



class UserListView(ListView):
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:login')  # Redirect to login page after successful registration


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list')  # Redirect to user list after successful update
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        return redirect('users:list')

class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:list')  # Redirect to user list after successful deletion
    def test_func(self):
        return self.get_object() == self.request.user
    
    def handle_no_permission(self):
        return redirect('users:list')  
