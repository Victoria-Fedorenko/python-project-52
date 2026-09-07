from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import StatusForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Status  # если модель в этом же приложении

# Create your views here.
class StatusListView(LoginRequiredMixin, ListView):

    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, CreateView):

    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(response, 'Статус успешно создан')
        return response

class StatusUpdateView(LoginRequiredMixin, UpdateView):

    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('statuses:list')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(response, 'Статус успешно изменен')
        return response

class StatusDeleteView(LoginRequiredMixin, DeleteView):

    model = Status
    template_name = 'statuses/confirm_delete.html'
    success_url = reverse_lazy('statuses:list')

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        if status.tasks.exists(): 
            messages.error(request, "Невозможно удалить статус")
            return redirect('statuses:list')
        messages.success(request, "Статус успешно удален")
        return super().post(request, *args, **kwargs)


