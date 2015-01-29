from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Julius has heard about a really nice and new TO-DO list, so he heads to the url and expects to find the word "To-Do" in the browsers title
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')
		
		# After Julius has had a productive session putting all the things he has to do in an order, he quits his browser, shuts his PC down and gets some ice-cream.
		# tearDonw-method will quit the browser

if __name__ == '__main__':
	unittest.main(warnings='ignore')