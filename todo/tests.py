from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import ToDo

# Create your tests here.
class TestCreateShareToDo(TestCase):
    fixtures = ['accounts/fixtures/users.json']

    def test_approve_change_on_shared_todo(self):
        """
        test creat todo
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
            'todo': 1, # user1 todo
            'user': 3, # user2
            'permission': 'read/write'
        }
        response = self.client.post(url, data, follow=True)
        self.assertEqual(response.status_code, 200)

        # user2 making changes in todo shared with him
        user2 = User.objects.get(username='user2')
        self.client.force_login(user2)

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
        updated_title = 'user1 todo updated'
        todo1 = get_object_or_404(ToDo, pk=1)
        self.assertEqual(todo1.title, updated_title)
