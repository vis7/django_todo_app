from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import ToDo

# Create your tests here.
class TestCreateShareToDo(TestCase):
    fixtures = ['accounts/fixtures/users.json']

    def test_approve_change_on_shared_todo(self):
        """
        - user1 create todo, share it with user2
        - user2 make changes
        - user1 approve changes and now it is reflected in todo
        """
        # create todo request
        url = 'http://127.0.0.1:8000/todo/create'
        data = {
            'title': 'user1 todo',
            'description': 'test description',
            'category': 'general',
            'status': False, # by default
            'due_date': '2023-02-10'
        }

        user1 = User.objects.get(username='user1')
        self.client.force_login(user1) # user authenticate
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # share todo request
        url = 'http://127.0.0.1:8000/todo/share_todo'
        data = {
            'todo': 1, # user1 todo, it will be the first created todo
            'user': 3, # user2
            'permission': 'read/write'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # user2 making changes in todo shared with him
        user2 = User.objects.get(username='user2')
        self.client.force_login(user2)

        # it will be first todo object created, so pk=1
        url = 'http://127.0.0.1:8000/todo/make_changes/1' 
        data = {
            'title': 'user1 todo updated',
            'description': 'test description',
            'category': 'general',
            'status': False, # by default
            'due_date': '2023-02-10'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # user1 approving the changes made by user1
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)

        url = 'http://127.0.0.1:8000/todo/compare_changes/1'
        data = {
            'action': 'approved'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # verify that user2 modification are actually applied
        content = response.content.decode('utf-8')
        self.assertTrue('updated' in content)

    def test_reject_change_on_shared_todo(self):
        """
        - user2 create todo, share it with user1
        - user1 make changes
        - user2 approve changes and now it is reflected in todo
        """
        # create todo request
        url = 'http://127.0.0.1:8000/todo/create'
        data = {
            'title': 'user2 todo',
            'description': 'test description',
            'category': 'general',
            'status': False, # by default
            'due_date': '2023-02-10'
        }

        user2 = User.objects.get(username='user2')
        self.client.force_login(user2) # user authenticate
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # share todo request
        url = 'http://127.0.0.1:8000/todo/share_todo'
        data = {
            'todo': 1, # user2 todo, it will be the first created todo
            'user': 2, # user1
            'permission': 'read/write'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # user1 making changes in todo shared with him
        user1 = User.objects.get(username='user1')
        self.client.force_login(user1)

        # it will be first todo object created, so pk=1
        url = 'http://127.0.0.1:8000/todo/make_changes/1' 
        data = {
            'title': 'user2 todo updated',
            'description': 'test description',
            'category': 'general',
            'status': False, # by default
            'due_date': '2023-02-10'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # user2 approving the changes made by user1
        user2 = User.objects.get(username='user2')
        self.client.force_login(user2)

        url = 'http://127.0.0.1:8000/todo/compare_changes/1'
        data = {
            'action': 'rejected'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # verify that user2 modification are actually applied
        content = response.content.decode('utf-8')
        self.assertTrue('updated' not in content)
