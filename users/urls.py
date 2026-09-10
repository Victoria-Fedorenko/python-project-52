from .views import (
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    UserLoginView,
    user_logout_view
)
from django.urls import path

app_name = 'users'  # пространство имён для обратных ссылок

urlpatterns = [
    # Список пользователей
    path('', UserListView.as_view(), name='list'),
    # Создание пользователя
    path('create/', UserCreateView.as_view(), name='create'),
    # Обновление пользователя
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    # Удаление пользователя
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
    # Вход
    path('login/', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    # Выход
    path('logout/', user_logout_view, name='logout'),
]