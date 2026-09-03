from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersTests(TestCase):

    fixtures = ['users.json'] 

    def test_users_list(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200) #check status code
        self.assertIn('users', response.context)
        users = response.context['users']
        self.assertEqual(users.count(), 2)
        usernames = [user.username for user in users]
        self.assertIn('alice', usernames)
        self.assertIn('bob', usernames)


    def test_correct_users_create(self):

        user_data = {
            'username': 'new_user',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'lala!!Un11',
            'password2': 'lala!!Un11'
            }     
        
        response = self.client.post(reverse('users:create'), user_data)
        self.assertTrue(User.objects.filter(username='new_user').exists())
        self.assertRedirects(response, '/')
        response = self.client.get(reverse('users:list'))
        users = response.context['users']
        usernames = [user.username for user in users]
        self.assertIn('new_user', usernames)

    def test_wrong_password_users_create(self):

        user_data = {
            'username': 'new_user',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'lala!!Un11',
            'password2': 'lala!!Un12'
            } 

        response = self.client.post(reverse('users:create'), user_data)
        self.assertFalse(User.objects.filter(username='new_user').exists())
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('password2'))

    def test_already_exist_users_create(self):

        user_data = {
            'username': 'alice',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'lala!!Un11',
            'password2': 'lala!!Un11'
            } 

        response = self.client.post(reverse('users:create'), user_data)
        self.assertEqual(User.objects.filter(username='alice').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('username'))

    def test_empty_username_users_create(self):

        user_data = {
            'username': '',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'lala!!Un11',
            'password2': 'lala!!Un11'
            }

        response = self.client.post(reverse('users:create'), user_data)
        self.assertEqual(User.objects.filter(username='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('username'))

    def test_get_users_update(self):

        self.client.login(username='alice', password='alicepass123')
        response = self.client.get(reverse('users:update', args=[2]))  # или pk alice
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')

    def test_correct_users_update(self):

        self.client.login(username='alice', password='alicepass123')

        updated_data = {
            'username': 'alice_updated',
            'first_name': 'Alice Updated',
            'last_name': 'Wonder',
            'password1': 'newpass123',
            'password2': 'newpass123',
        }

        response = self.client.post(reverse('users:update', args=[2]), updated_data)
        self.assertRedirects(response, reverse('users:list'))
        user = User.objects.get(id=2)
        self.assertEqual(user.username, 'alice_updated')
        self.assertEqual(user.first_name, 'Alice Updated')
        self.assertEqual(user.last_name, 'Wonder')
        users = response.context['users']
        self.assertEqual(users.count(), 2)
        usernames = [user.username for user in users]
        self.assertIn('alice_updated', usernames)

    def test_wrong_password_users_update(self):

        self.client.login(username='alice', password='alicepass123')
        
        updated_data = {
            'username': 'alice_updated',
            'first_name': 'Alice Updated',
            'last_name': 'Wonder',
            'password1': 'newpass123',
            'password2': 'newpass133',
            } 

        response = self.client.post(reverse('users:update', args=[2]), updated_data)
        self.assertFalse(User.objects.filter(username='alice_updated').exists())
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('password2'))

    def test_already_taken_users_update(self):

        self.client.login(username='alice', password='alicepass123')

        updated_data = {
            'username': 'bob',
            'first_name': 'Alice Updated',
            'last_name': 'Wonder',
            'password1': 'newpass123',
            'password2': 'newpass123',
            } 

        response = self.client.post(reverse('users:update', args=[2]), updated_data)
        self.assertEqual(User.objects.filter(username='bob').count(), 1)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('username'))

    def test_empty_username_users_update(self):

        self.client.login(username='alice', password='alicepass123')

        updated_data = {
            'username': '',
            'first_name': 'Alice Updated',
            'last_name': 'Wonder',
            'password1': 'newpass123',
            'password2': 'newpass123',
            } 

        response = self.client.post(reverse('users:update', args=[2]), updated_data)
        self.assertEqual(User.objects.filter(username='').count(), 0)
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.errors.get('username'))

    def test_user_delete_get(self):

        self.client.login(username='alice', password='alicepass123')
        response = self.client.get(reverse('users:delete', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='alice').exists())
        self.assertTemplateUsed(response, 'users/user_confirm_delete.html')

    def test_user_delete_requires_login(self):

        self.client.logout()
        response = self.client.get(reverse('users:delete', args=[2]))
        self.assertRedirects(response, f'/users/login/?next=/users/2/delete/')
        self.assertTrue(User.objects.filter(username='alice').exists())

    def test_user_delete_other_user_forbidden(self):
        """Пользователь не может удалить другого"""
        # Логинимся как alice (pk=2)
        self.client.login(username='alice', password='alicepass123')
        
        # Пытаемся удалить bob (pk=3)
        response = self.client.get(reverse('users:delete', args=[3]))
        
        # Проверяем редирект на список (если так настроили handle_no_permission)
        self.assertRedirects(response, reverse('users:list'))
        
        # Проверяем, что bob всё ещё существует
        self.assertTrue(User.objects.filter(username='bob').exists())

    def test_user_delete_self_allowed(self):

        self.client.login(username='alice', password='alicepass123')
        
        response = self.client.post(reverse('users:delete', args=[2]))
        
        self.assertRedirects(response, reverse('users:list'))
        self.assertFalse(User.objects.filter(username='alice').exists())







    



