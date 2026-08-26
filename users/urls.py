from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'users'  # пространство имён для обратных ссылок

urlpatterns = [
    # Список пользователей
    path('', UserListView.as_view(), name='list'),
    
    # Создание пользователя
    path('create/', UserCreateView.as_view(), name='create'),
    # Редактирование пользователя
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update')]