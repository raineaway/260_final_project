from selenium import webdriver
from django.contrib.auth.models import User
import unittest

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        User.objects.all().delete()

    def test_can_signup(self):
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

        # clicking on Create an Account should redirect to sign up page
        #self.browser.find_element_by_link_text('Create an Account').click()
        #self.browser.implicitly_wait(3)
        #self.assertEqual('http://localhost:8000/signup', self.browser.current_url)

        # sign up page should contain the sign up form
        #self.assertEqual('Sign Up | To-Do List', self.browser.title)

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
