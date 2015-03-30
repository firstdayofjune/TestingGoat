from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		#self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Julius has heard about a really nice and new TO-DO list, so he heads to the url and expects to find the word "To-Do" in the browsers title
		self.browser.get('http://localhost:8000')
		self.assertIn('To-Do', self.browser.title)

		# He spots the first headline, where it says 'To-Do' ...
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
		
		# ... and is prompted to enter his first to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'), 
			'Enter a to-do item'
			)

		# He types 'Buy peacock feathers' into a text box and hits the enter button
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)

		# Since there still is an input-field to enter items, Julius enters 'Use peacock feathers to make a fly'
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)		

		# Now the recently added to-do item is shown in the to-do list table
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
		self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

		# There now still is a input-box, where new to-do items can be added
		self.fail('Finish the test!')
		# After Julius has had a productive session putting all the things he has to do in an order, he quits his browser, shuts his PC down and gets some ice-cream.
		# tearDonw-method will quit the browser

if __name__ == '__main__':
	unittest.main(warnings='ignore')