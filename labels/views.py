from django.contrib import messages, redirects
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Label
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LabelForm

# Create your views here.
class LabelListView(LoginRequiredMixin, ListView):

    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'

class LabelCreateView(LoginRequiredMixin, CreateView):

    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:list')

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('labels:list')

class LabelDeleteView(LoginRequiredMixin, DeleteView):

    model = Label
    template_name = 'labels/confirm_delete.html'
    success_url = reverse_lazy('labels:list')

    def post(self, request, *args, **kwargs):
        if self.get_object().tasks.exists():
            messages.error(self.request, 'Невозможно удалить метку')
            return redirects('labels:list')
        messages.success(self.request, 'Метка успешно удалена')
        return super().post(self.request, *args, **kwargs)