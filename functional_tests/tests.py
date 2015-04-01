from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		#self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Julius has heard about a really nice and new TO-DO list, so he heads to the url and expects to find the word "To-Do" in the browsers title
		self.browser.get(self.live_server_url)
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
		# The site takes him to a new URL, where 'Buy peacock feathers' will be listed
		inputbox.send_keys('Buy peacock feathers')
		inputbox.send_keys(Keys.ENTER)
		julius_list_url = self.browser.current_url
		self.assertRegex(julius_list_url, 'lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		
		# Since there still is an input-field to enter items, Julius enters 'Use peacock feathers to make a fly'
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)		
		# The page updates and the two to do items are displayed in an enumerated list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# After Julius has had a productive session putting all the things he has to do in an order,
		# he quits his browser, shuts his PC down and gets some ice-cream.
		self.browser.quit()

		## A new user Edith comes along, of course Edith uses a new browser session #
		## (also to make sure that no information of Julius' comes from cookies) #
		self.browser = webdriver.Firefox()
		
		# She visits the website, where no sign of Julius' to-do list is left
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		
		# Edith starts a new list by entering an item
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)		

		# Again, Edith gets his own unique URL, which is definately different from Julius'
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, 'lists/.+')
		self.assertNotEqual(edith_list_url, julius_list_url)
		
		# There is no trace of Julius' list, but her first item is displayed instead
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		self.assertIn('1: Buy milk', page_text)

		# Satisfied, Edith can go to bed now.