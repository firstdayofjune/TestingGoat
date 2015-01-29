from selenium import webdriver

browser = webdriver.Opera()
browser.get('http://localhost:8000')

assert 'Django' in browser.title