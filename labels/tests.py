from django.test import TestCase
from django.urls import reverse
from users.models import User
from statuses.models import Status
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from tasks.models import Task
from labels.models import Label 

# Create your tests here.
class LabelsTests(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create_user(username='test_user', password='lol1997!')
        cls.status = Status.objects.create(name='test_status')
        cls.label_with_task = Label.objects.create(name='label_with_task')
        cls.label_without_task = Label.objects.create(name='label_without_task')
        cls.task = Task.objects.create(name='test_task', status=cls.status, author=cls.user)
        cls.task.labels.add(cls.label_with_task)

    def test_get_labels_authorized(self):

        self.client.force_login(self.user)
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        labels = response.context['labels']
        self.assertEqual(labels.count(), 2)
        self.assertIn(self.label_with_task, labels)
        self.assertIn(self.label_without_task, labels)

    def test_get_labels_logout(self):

        self.client.logout()
        response = self.client.get(reverse('labels:list'))
        self.assertRedirects(response, f'/users/login/?next=/labels/')

    def test_label_create(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:create'), {'name': 'test_label'})
        self.assertTrue(Label.objects.filter(name='test_label').count() == 1)
        self.assertRedirects(response, reverse('labels:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно создана")

    def test_label_create_logout(self):

        self.client.logout()
        response = self.client.get(reverse('labels:create'))
        self.assertRedirects(response, f'/users/login/?next=/labels/create/')
        response = self.client.post(reverse('labels:create'), {'name': 'test_label'})
        self.assertTrue(Label.objects.filter(name='test_label').count() == 0)
        self.assertRedirects(response, f'/users/login/?next=/labels/create/')

    def test_label_create_empty(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:create'), {'name': ''})
        self.assertEqual(Label.objects.filter(name='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_label_create_already_taken(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:create'), {'name': 'label_without_task'})
        self.assertEqual(Label.objects.filter(name='label_without_task').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_label_update(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:update', args=[self.label_without_task.id]), {'name': 'label'})
        self.assertTrue(Label.objects.filter(name='label').count() == 1)
        self.assertRedirects(response, reverse('labels:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно изменена")

    def test_label_update_logout(self):

        self.client.logout()
        response = self.client.get(reverse('labels:update', args=[self.label_without_task.id]))
        self.assertRedirects(response, f'/users/login/?next=/labels/{self.label_without_task.id}/update/')
        response = self.client.post(reverse('labels:update', args=[self.label_without_task.id]), {'name': 'test_label'})
        self.assertTrue(Label.objects.filter(name='test_label').count() == 0)
        self.assertRedirects(response, f'/users/login/?next=/labels/{self.label_without_task.id}/update/')

    def test_label_update_empty(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:update', args=[self.label_without_task.id]), {'name': ''})
        self.assertEqual(Label.objects.filter(name='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_label_update_already_taken(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:update', args=[self.label_without_task.id]), {'name': 'label_with_task'})
        self.assertEqual(Label.objects.filter(name='label_with_task').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('name'))

    def test_label_delete_logout(self):

        self.client.logout()
        response = self.client.get(reverse('labels:delete', args=[self.label_without_task.id]))
        self.assertRedirects(response, f'/users/login/?next=/labels/{self.label_without_task.id}/delete/')
        response = self.client.post(reverse('labels:delete', args=[self.label_without_task.id]))
        self.assertTrue(Label.objects.filter(name='label_without_task').count() == 1)
        self.assertRedirects(response, f'/users/login/?next=/labels/{self.label_without_task.id}/delete/')

    def test_label_no_tasks_delete(self):

        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:delete', args=[self.label_without_task.id]))
        self.assertTrue(Label.objects.filter(name='label_without_task').count() == 0)
        self.assertRedirects(response, reverse('labels:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно удалена")

    def test_label_with_tasks_delete(self):
        
        self.client.force_login(self.user)
        response = self.client.post(reverse('labels:delete', args=[self.label_with_task.id]))
        self.assertTrue(Label.objects.filter(name='label_with_task').count() == 1)
        self.assertRedirects(response, reverse('labels:list'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Невозможно удалить метку")
