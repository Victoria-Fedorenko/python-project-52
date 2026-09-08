from django import forms
from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):

    class Meta:

        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'})
        }      