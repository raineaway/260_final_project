from django.test import Client
from django.contrib.auth.models import User
from lists.models import Item
from django.utils import timezone
import unittest
import datetime

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

    def create_item(self):
        response = self.client.post('/create_item', {'task_name':'Test item'}, follow=True)
        return response

    def create_superuser(self):
        user = User.objects.create_superuser("admin", "admin@admin.org", "pass")
        return user

    def login_superuser(self, admin):
        response = self.client.login(username='admin', password='pass')
        self.assertTrue(response)
        response = self.client.get('/admin/', follow=True)

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

        self.assertIn('Hello, Raine', response.content)

    def test_create_item(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

        response = self.create_item()
        self.assertEqual(response.status_code, 200)
        item = Item.objects.get(name="Test item")
        user = User.objects.get(username="raineaway")
        self.assertTrue(Item.objects.filter(name="Test item").exists())
        self.assertEqual(item.user_id, user.id)

        self.assertIn('Test item', response.content)

    def test_check_item(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

        response = self.create_item()
        self.assertEqual(response.status_code, 200)
        item = Item.objects.get(name="Test item")

        response = self.client.post('/check_item', {'id':item.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"status": "ok"}', response.content)

        item = Item.objects.get(name="Test item")
        self.assertEqual('done', item.status)

    def test_uncheck_item(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

        response = self.create_item()
        self.assertEqual(response.status_code, 200)

        item = Item.objects.get(name="Test item")
        response = self.client.post('/check_item', {'id':item.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"status": "ok"}', response.content)

        item = Item.objects.get(name="Test item")
        self.assertEqual('done', item.status)

        response = self.client.post('/check_item', {'id':item.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"status": "ok", "item_status": "pending"}', response.content)

        item = Item.objects.get(name="Test item")
        self.assertEqual('pending', item.status)

    def test_cancel_item(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

        response = self.create_item()
        self.assertEqual(response.status_code, 200)

        item = Item.objects.get(name="Test item")
        response = self.client.post('/cancel_item', {'id':item.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual('{"status": "ok"}', response.content)

    def test_filter_items(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 200)
        
        response = self.login_user()
        self.assertEqual(response.status_code, 200)

        response = self.create_item()
        self.assertEqual(response.status_code, 200)

        item = Item.objects.get(name="Test item")
        user_id = item.user_id
        user = User.objects.get(id=user_id)

        yesterday = datetime.datetime.now() + datetime.timedelta(days=-1)
        item2 = Item(user=user, name="Another test", date_created=yesterday, date_modified=yesterday)
        item2.save()

        response = self.client.get('/')
        self.assertIn('Test item', response.content)
        self.assertIn('Another test', response.content)

        item2 = Item.objects.get(name="Another test")
        item2.status = "done"
        item2.date_modified = yesterday
        item2.save()

        response = self.client.get('/')
        self.assertIn('Test item', response.content)
        self.assertNotIn('Another test', response.content)

        response = self.client.get('/?date=-1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Another test', response.content)
        self.assertNotIn('Test item', response.content)

    def test_admin(self):
        user = self.create_superuser()
        admin = User.objects.get(username='admin')
        self.assertEqual('admin', admin.username)
        self.assertEqual(True, admin.is_superuser)

        response = self.login_superuser(user)
        self.assertEqual(response.status_code, 200)

        self.assertIn('model-user', response.content)
        self.assertIn('app-lists module', response.content)
        self.assertIn('model-item', response.content)

        response = self.client.get('/admin/auth/user/')
        self.assertEqual(response.status_code, 200)

        self.assertIn('admin@admin.org', response.content)

        test_user = User.objects.create_user("test_user", "test@test.org", "test")

        response = self.client.get('/admin/auth/user/')
        self.assertIn('test@test.org', response.content)

        response = self.client.get('/admin/auth/user/' + str(test_user.id), follow=True)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/admin/lists/item/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
