from django.test import Client
from django.contrib.auth.models import User
import unittest

class UnitTest(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def register_user(self):
        response = self.client.post('/signup',
            {'name':'Raine', 'username':'raineaway', 'email':'ltedrosa@gmail.com', 'password':'pass', 'confirm_password':'pass'})
        return response

    def login_user(self):
        response = self.client.post('/signin', {'username':'raineaway', 'password':'pass'}, follow=True)
        return response

    def test_home_guest(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to To-Do List!', response.content)
        self.assertIn('<input type="text" name="name" placeholder="Name" />', response.content)
        self.assertIn('<input type="text" name="username" placeholder="Username" />', response.content)
        self.assertIn('<input type="text" name="email" placeholder="Email" />', response.content)
        self.assertIn('<input type="password" name="password" placeholder="Password" />', response.content)
        self.assertIn('<input type="password" name="confirm_password" placeholder="Confirm Password" />', response.content)
        self.assertIn('<input type="submit" value="Create an Account" class="submit" />', response.content)

        self.assertIn('Have an account?', response.content)
        self.assertIn('<a href="signin" class="login">Log In</a>', response.content)

    def test_register_user(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username="raineaway")
        self.assertEqual(user.email, 'ltedrosa@gmail.com')
        self.assertEqual(user.first_name, 'Raine')

    def test_login_user(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

        

if __name__ == '__main__':
    unittest.main(warnings='ignore')
