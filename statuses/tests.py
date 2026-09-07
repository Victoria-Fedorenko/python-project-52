from django.test import TestCase
from django.urls import reverse
from .models import Status
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from tasks.models import Task


# Create your tests here.
class StatusesTests(TestCase):

    User = get_user_model()

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='test_user', password='lol1997!')
        cls.status1 = Status.objects.create(name='new')
        cls.status2 = Status.objects.create(name='in progress')
        cls.status3 = Status.objects.create(name='status_with_task')
        cls.task = Task.objects.create(name='test_task', status=cls.status3, author=cls.user)

    def test_get_statuses_list_authorized(self):

        self.client.force_login(self.user)
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        statuses = response.context['statuses']
        self.assertEqual(statuses.count(), 3)
        self.assertIn(self.status1, statuses)
        self.assertIn(self.status2, statuses)
        self.assertIn(self.status3, statuses)

    def test_get_statuses_list_logout(self):

        self.client.logout()
        response = self.client.get(reverse('statuses:list'))
        self.assertRedirects(response, f'/users/login/?next=/statuses/list/')

    def test_status_create(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:create'), {'name': 'test_status'})
        self.assertTrue(Status.objects.filter(name='test_status').count() == 1)
        self.assertRedirects(response, reverse('statuses:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно создан")

    def test_status_create_logout(self):

        self.client.logout()
        response = self.client.get(reverse('statuses:create'))
        self.assertRedirects(response, f'/users/login/?next=/statuses/create/')
        response = self.client.post(reverse('statuses:create'), {'name': 'test_status'})
        self.assertTrue(Status.objects.filter(name='test_status').count() == 0)
        self.assertRedirects(response, f'/users/login/?next=/statuses/create/')

    def test_status_create_empty(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:create'), {'name': ''})
        self.assertEqual(Status.objects.filter(name='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_status_create_already_taken(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:create'), {'name': 'in progress'})
        self.assertEqual(Status.objects.filter(name='in progress').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_status_update(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:update', args=[self.status1.id]), {'name': 'new_updated'})
        self.assertTrue(Status.objects.filter(name='new_updated').count() == 1)
        self.assertRedirects(response, reverse('statuses:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно изменен")

    def test_status_update_logout(self):

        self.client.logout()
        response = self.client.get(reverse('statuses:update', args=[self.status1.id]))
        self.assertRedirects(response, f'/users/login/?next=/statuses/{self.status1.id}/update/')
        response = self.client.post(reverse('statuses:update', args=[self.status1.id]), {'name': 'test_status'})
        self.assertTrue(Status.objects.filter(name='test_status').count() == 0)
        self.assertRedirects(response, f'/users/login/?next=/statuses/{self.status1.id}/update/')

    def test_status_update_empty(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:update', args=[self.status1.id]), {'name': ''})
        self.assertEqual(Status.objects.filter(name='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_status_update_already_taken(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:update', args=[self.status1.id]), {'name': 'in progress'})
        self.assertEqual(Status.objects.filter(name='in progress').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_status_delete_logout(self):

        self.client.logout()
        response = self.client.get(reverse('statuses:delete', args=[self.status2.id]))
        self.assertRedirects(response, f'/users/login/?next=/statuses/{self.status2.id}/delete/')
        response = self.client.post(reverse('statuses:delete', args=[self.status2.id]))
        self.assertTrue(Status.objects.filter(name='in progress').count() == 1)
        self.assertRedirects(response, f'/users/login/?next=/statuses/{self.status2.id}/delete/')

    def test_status_no_tasks_delete(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:delete', args=[self.status2.id]))
        self.assertTrue(Status.objects.filter(name='in progress').count() == 0)
        self.assertRedirects(response, reverse('statuses:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно удален")

    def test_status_with_tasks_delete(self):
        
        self.client.force_login(self.user)
        response = self.client.post(reverse('statuses:delete', args=[self.status3.id]))
        self.assertTrue(Status.objects.filter(name='status_with_task').count() == 1)
        self.assertRedirects(response, reverse('statuses:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Невозможно удалить статус")

