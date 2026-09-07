from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
)
from django.urls import path    

app_name = 'tasks'  # пространство имён для обратных ссылок

urlpatterns = [
    path('', TaskListView.as_view(), name='list'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='delete'),
    path('<int:pk>/', TaskDetailView.as_view(), name='detail'),
    ]   