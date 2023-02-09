from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.
class TestCreateShareToDo(TestCase):

    def test_create_todo(self):
        """
        test creat todo
        """
        url = 'http://127.0.0.1:8000/todo/create' # post
        data = {
            'title': 'user3 todo',
            'description': 'test description',
            'category': 'general',
            'status': False, # by default
            'due_date': '2023-02-10'
        }

        # user authenticate
        user3 = User.objects.get(username='user3')
        print(user3)
        self.client.force_authenticate(user=user3)
        # self.client.force_authenticate(user=user1)

        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code == 200)

