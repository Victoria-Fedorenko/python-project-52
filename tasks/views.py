from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Task  
from .filters import TaskFilter


class TaskListView(LoginRequiredMixin, ListView):

    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        self.filterset = TaskFilter(
            self.request.GET,
            queryset=super().get_queryset(),
            request=self.request
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset #дополняем данные объектом фильтра
        return context
    

class TaskCreateView(LoginRequiredMixin, CreateView):

    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно создана')
        return response

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Задача успешно изменена')
        return response

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/confirm_delete.html'
    success_url = reverse_lazy('tasks:list')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks:list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно удалена')
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):

    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'