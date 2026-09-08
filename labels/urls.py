from .views import (
    LabelListView,
    LabelCreateView,    
    LabelUpdateView,
    LabelDeleteView,
)

from django.urls import path  

app_name = 'labels'  # пространство имён для обратных ссылок

urlpatterns = [
    path('', LabelListView.as_view(), name='list'),
    path('create/', LabelCreateView.as_view(), name='create'),
    path('<int:pk>/update/', LabelUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', LabelDeleteView.as_view(), name='delete'),
    ]   
