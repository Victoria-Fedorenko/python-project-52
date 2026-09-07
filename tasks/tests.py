from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from .models import Task
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages


class TasksTest(TestCase):

    User = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.user_author = User.objects.create_user(username='user_author', password='lol1997!')
        cls.user_executor = User.objects.create_user(username='user_executor', password='heh1997!')
        cls.status1 = Status.objects.create(name='new')
        cls.status2 = Status.objects.create(name='in progress')
        cls.task1 = Task.objects.create(
            name='task1',
            status=cls.status1,
            author=cls.user_author,
            executor=cls.user_executor
        )
        cls.task2 = Task.objects.create(
            name='task2',
            status=cls.status2,
            author=cls.user_author,
            executor=cls.user_executor
        )

    # ----- СПИСОК ЗАДАЧ -----
    def test_get_tasks_list(self):
        self.client.force_login(self.user_author)
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        tasks = response.context['tasks']
        self.assertEqual(tasks.count(), 2)
        self.assertIn(self.task1, tasks)
        self.assertIn(self.task2, tasks)

    def test_get_tasks_list_logout(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:list'))
        self.assertRedirects(response, '/users/login/?next=/tasks/')

    # ----- СОЗДАНИЕ ЗАДАЧИ -----
    def test_task_create(self):
        task_data = {
            'name': 'ok_task',
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.force_login(self.user_author)
        response = self.client.post(reverse('tasks:create'), task_data)
        self.assertEqual(Task.objects.filter(name='ok_task').count(), 1)
        self.assertRedirects(response, reverse('tasks:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно создана")
        created_task = Task.objects.get(name='ok_task')
        self.assertEqual(created_task.author, self.user_author)

    def test_task_create_logout(self):
        task_data = {
            'name': 'bad_task',
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.logout()
        # Проверяем GET-доступ (страница создания)
        response = self.client.get(reverse('tasks:create'))
        self.assertRedirects(response, '/users/login/?next=/tasks/create/')
        # Проверяем POST (создание)
        response = self.client.post(reverse('tasks:create'), task_data)
        self.assertEqual(Task.objects.filter(name='bad_task').count(), 0)
        self.assertRedirects(response, '/users/login/?next=/tasks/create/')

    def test_task_create_name_already_taken(self):
        task_data = {
            'name': 'task1',  # уже существует
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.force_login(self.user_author)
        response = self.client.post(reverse('tasks:create'), task_data)
        self.assertEqual(Task.objects.filter(name='task1').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_task_create_name_empty(self):
        task_data = {
            'name': '',
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.force_login(self.user_author)
        response = self.client.post(reverse('tasks:create'), task_data)
        self.assertEqual(Task.objects.filter(name='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    # ----- ОБНОВЛЕНИЕ ЗАДАЧИ -----
    def test_task_update(self):
        task_data = {
            'name': 'task1_updated',
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.force_login(self.user_executor)  # любой залогиненный может обновить
        response = self.client.post(
            reverse('tasks:update', args=[self.task1.id]),
            task_data
        )
        self.assertEqual(Task.objects.filter(name='task1_updated').count(), 1)
        self.assertRedirects(response, reverse('tasks:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно изменена")

    def test_task_update_logout(self):
        task_data = {
            'name': 'task1_updated_bad',
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.logout()
        # GET-запрос на страницу обновления
        response = self.client.get(reverse('tasks:update', args=[self.task1.id]))
        self.assertRedirects(response, f'/users/login/?next=/tasks/{self.task1.id}/update/')
        # POST-запрос с данными
        response = self.client.post(
            reverse('tasks:update', args=[self.task1.id]),
            task_data
        )
        self.assertEqual(Task.objects.filter(name='task1_updated_bad').count(), 0)
        self.assertRedirects(response, f'/users/login/?next=/tasks/{self.task1.id}/update/')

    def test_task_update_name_already_taken(self):
        task_data = {
            'name': 'task2',  # уже существует
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.force_login(self.user_author)
        response = self.client.post(
            reverse('tasks:update', args=[self.task1.id]),
            task_data
        )
        self.assertEqual(Task.objects.filter(name='task1').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_task_update_name_empty(self):
        task_data = {
            'name': '',
            'status': self.status1.pk,
            'executor': self.user_executor.pk
        }
        self.client.force_login(self.user_author)
        response = self.client.post(
            reverse('tasks:update', args=[self.task1.id]),
            task_data
        )
        self.assertEqual(Task.objects.filter(name='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    # ----- УДАЛЕНИЕ ЗАДАЧИ -----
    def test_task_delete_logout(self):
        self.client.logout()
        # GET-запрос на страницу удаления
        response = self.client.get(reverse('tasks:delete', args=[self.task2.id]))
        self.assertRedirects(response, f'/users/login/?next=/tasks/{self.task2.id}/delete/')
        # POST-запрос на удаление
        response = self.client.post(reverse('tasks:delete', args=[self.task2.id]))
        self.assertEqual(Task.objects.filter(name='task2').count(), 1)
        self.assertRedirects(response, f'/users/login/?next=/tasks/{self.task2.id}/delete/')

    def test_task_delete_author(self):
        # Автор может удалить свою задачу
        self.client.force_login(self.user_author)
        response = self.client.post(reverse('tasks:delete', args=[self.task2.id]))
        self.assertEqual(Task.objects.filter(name='task2').count(), 0)
        self.assertRedirects(response, reverse('tasks:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задача успешно удалена")

    def test_task_delete_executor(self):
        # Исполнитель (не автор) НЕ может удалить задачу
        self.client.force_login(self.user_executor)
        response = self.client.post(reverse('tasks:delete', args=[self.task1.id]))
        self.assertEqual(Task.objects.filter(name='task1').count(), 1)
        self.assertRedirects(response, reverse('tasks:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Задачу может удалить только ее автор")

    # ----- ПРОСМОТР ЗАДАЧИ -----
    def test_get_task_detail(self):
        self.client.force_login(self.user_author)
        response = self.client.get(reverse('tasks:detail', args=[self.task1.id]))
        self.assertEqual(response.status_code, 200)

    def test_get_task_detail_logout(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:detail', args=[self.task1.id]))
        self.assertRedirects(response, f'/users/login/?next=/tasks/{self.task1.id}/')