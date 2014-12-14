from selenium import webdriver
import unittest

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_signup(self):
        # check homepage
        self.browser.get('http://localhost:8000')

        # page should load the To-Do List landing page
        self.assertIn('To-Do List', self.browser.title)

        self.assertIn('Welcome to To-Do List!', self.browser.find_element_by_tag_name("body").text);
        self.assertIn('Create an Account', self.browser.find_element_by_tag_name("body").text);
        self.assertIn('Log In', self.browser.find_element_by_tag_name("body").text);

        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')
