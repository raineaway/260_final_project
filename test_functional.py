from selenium import webdriver
from django.contrib.auth.models import User
import unittest

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.get('http://localhost:8000/delete_test')
        self.browser.quit()
        User.objects.all().delete()

    def Test_signup(self):
        # check homepage
        self.browser.get('http://localhost:8000')

        # page should load the To-Do List landing page
        self.assertIn('To-Do List', self.browser.title)
        self.assertIn('Welcome to To-Do List!', self.browser.find_element_by_tag_name("body").text)
        #self.assertIn('Create an Account', self.browser.find_element_by_tag_name("body").text)
        #self.assertIn('Log In', self.browser.find_element_by_tag_name("body").text)

        # home page should contain sign up form, for easier and faster sign up for new users
        self.assertTrue(self.browser.find_element_by_name("name").size > 1)
        self.assertTrue(self.browser.find_element_by_name("username").size > 1)
        self.assertTrue(self.browser.find_element_by_name("email").size > 1)
        self.assertTrue(self.browser.find_element_by_name("password").size > 1)
        self.assertTrue(self.browser.find_element_by_name("confirm_password").size > 1)
        self.assertTrue(self.browser.find_element_by_class_name("submit").size > 1)

        # fill up and submit the form (valid input first)
        self.browser.find_element_by_name("name").send_keys("Raine")
        self.browser.find_element_by_name("username").send_keys("raineaway")
        self.browser.find_element_by_name("email").send_keys("ltedrosa@gmail.com")
        self.browser.find_element_by_name("password").send_keys("password")
        self.browser.find_element_by_name("confirm_password").send_keys("password")
        self.browser.find_element_by_class_name("submit").click()

        # after submitting, should be redirected to successfully signed up page
        self.browser.implicitly_wait(3)
        self.assertEqual('http://localhost:8000/signup', self.browser.current_url)
        self.assertEqual('Welcome to To-Do List, Raine! | To-Do List', self.browser.title)
        self.assertIn('Congratulations! You have successfully signed up.', self.browser.find_element_by_tag_name("body").text)
        self.assertIn('Start my to-do list', self.browser.find_element_by_tag_name("body").text)

        # click on Start my to-do list; should be redirected to home page, but this time user must be logged in already.
        self.browser.find_element_by_tag_name("a").click()
        self.browser.implicitly_wait(3)
        self.assertIn('http://localhost:8000', self.browser.current_url)
        self.assertIn('Hello, Raine', self.browser.find_element_by_tag_name("body").text)

        # manually delete created user in production
        self.browser.get('http://localhost:8000/delete_test')

        # clicking on Create an Account should redirect to sign up page
        #self.browser.find_element_by_link_text('Create an Account').click()
        #self.browser.implicitly_wait(3)
        #self.assertEqual('http://localhost:8000/signup', self.browser.current_url)

        # sign up page should contain the sign up form
        #self.assertEqual('Sign Up | To-Do List', self.browser.title)

        #self.fail('Finish the test!')

    def Test_login(self):
        self.browser.get('http://localhost:8000')
        # fill up and submit the form (valid input first)
        self.browser.find_element_by_name("name").send_keys("Raine")
        self.browser.find_element_by_name("username").send_keys("raineaway")
        self.browser.find_element_by_name("email").send_keys("ltedrosa@gmail.com")
        self.browser.find_element_by_name("password").send_keys("password")
        self.browser.find_element_by_name("confirm_password").send_keys("password")
        self.browser.find_element_by_class_name("submit").click()

        # after submitting, should be redirected to successfully signed up page
        self.browser.implicitly_wait(3)

        # click on Start my to-do list; should be redirected to home page, but this time user must be logged in already.
        self.browser.find_element_by_tag_name("a").click()
        self.browser.implicitly_wait(3)

        # click on logout link
        self.assertIn('Logout', self.browser.find_element_by_tag_name("body").text)
        self.browser.find_element_by_class_name("logout").click()

        # should be redirected to homepage with sign up form
        self.browser.implicitly_wait(3)
        self.assertIn('http://localhost:8000', self.browser.current_url)
        self.assertIn('Welcome to To-Do List!', self.browser.find_element_by_tag_name("body").text)
        self.assertTrue(self.browser.find_element_by_name("name").size > 1)
        self.assertTrue(self.browser.find_element_by_name("username").size > 1)
        self.assertTrue(self.browser.find_element_by_name("email").size > 1)
        self.assertTrue(self.browser.find_element_by_name("password").size > 1)
        self.assertTrue(self.browser.find_element_by_name("confirm_password").size > 1)
        self.assertTrue(self.browser.find_element_by_class_name("submit").size > 1)

        # click on login link
        self.browser.find_element_by_class_name("login").click()

        # should display the login form
        self.browser.implicitly_wait(3)
        self.assertIn('http://localhost:8000/signin', self.browser.current_url)
        self.assertIn('Sign In', self.browser.title)
        self.assertIn('Sign In with To-Do List', self.browser.find_element_by_tag_name("body").text)
        self.assertTrue(self.browser.find_element_by_name("username").size > 1)
        self.assertTrue(self.browser.find_element_by_name("password").size > 1)
        self.assertTrue(self.browser.find_element_by_class_name("submit").size > 1)

        # fill out form and submit
        self.browser.find_element_by_name("username").send_keys("raineaway")
        self.browser.find_element_by_name("password").send_keys("password")
        self.browser.find_element_by_class_name("submit").click()

        # should be redirected to the homepage
        self.browser.implicitly_wait(3)
        self.assertIn('http://localhost:8000', self.browser.current_url)
        self.assertIn('Hello, Raine', self.browser.find_element_by_tag_name("body").text)

        # manually delete created user in production
        self.browser.get('http://localhost:8000/delete_test')
        

    def Test_add_list_item(self):
        self.browser.get('http://localhost:8000')
        # fill up and submit the form (valid input first)
        self.browser.find_element_by_name("name").send_keys("Raine")
        self.browser.find_element_by_name("username").send_keys("raineaway")
        self.browser.find_element_by_name("email").send_keys("ltedrosa@gmail.com")
        self.browser.find_element_by_name("password").send_keys("password")
        self.browser.find_element_by_name("confirm_password").send_keys("password")
        self.browser.find_element_by_class_name("submit").click()

        # after submitting, should be redirected to successfully signed up page
        self.browser.implicitly_wait(3)

        # click on Start my to-do list; should be redirected to home page
        self.browser.find_element_by_tag_name("a").click()
        self.browser.implicitly_wait(3)

        self.assertIn('Today', self.browser.find_element_by_tag_name("body").text)
        self.assertIn(datetime.date.today(), self.browser.find_element_by_tag_name("body").text)

        self.assertIn('You have no to-do items yet.', self.browser.find_element_by_tag_name("body").text)
        self.assertIn('Create one now.', self.browser.find_element_by_tag_name("body").text)

        self.browser.find_element_by_class_name("create").click()

        self.browser.implicitly_wait(3)

        self.browser.assertIn('http://localhost:8000/create_item', self.browser.current_url)
        self.browser.assertIn('Create a Task', self.browser.find_element_by_tag_name("body").text)
        self.assertTrue(self.browser.find_element_by_name("task_name").size > 1)
        self.assertTrue(self.browser.find_element_by_xpath("//input[@value='Create']").size > 1)

        self.browser.find_element_by_name("task_name").send_keys("Finish the project")
        self.browser.find_element_by_xpath("//input[@value='Create']").click()
        
        self.browser.implicitly_wait(3)

        self.browser.assertIn('http://localhost:8000', self.browser.current_url)
        self.assertIn('Finish the project', self.browser.find_element_by_tag_name("body").text)

        self.browser.get('http://localhost:8000/delete_test')
        

    def test_order(self):
        self.Test_signup()
        self.Test_login()
        self.Test_add_list_item()

if __name__ == '__main__':
    unittest.main(warnings='ignore')
