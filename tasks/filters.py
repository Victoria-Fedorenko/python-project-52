import django_filters
from django import forms
from .models import Task
from statuses.models import Status
from users.models import User
from labels.models import Label

class TaskFilrer(django_filters.FilterSet):

        status = django_filters.ModelChoiceFilter(
                queryset=Status.objects.all(),
                empty_label='Все статусы')
        executor = django_filters.ModelChoiceFilter(
                queryset=User.objects.all(),
                empty_label='Все исполнители')
        labels = django_filters.ModelMultipleChoiceFilter(
                queryset=Label.objects.all(),
                widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
        author = django_filters.BooleanFilter(
                method='filter_author',
                widget=forms.CheckboxInput(),
                label='Только свои задачи')

        class Meta:

            model = Task
            fields = []

        def filter_author(self, queryset, name, value):
            if value:
                if hasattr(self, 'request') and self.request.user.is_authenticated:
                    return queryset.filter(author=self.request.user)
                return queryset