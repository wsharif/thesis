#!/usr/bin/env python

from bs4 import BeautifulSoup
from os.path import dirname, realpath
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

username = 'admin'
password = 'admin'
ipAddress = '127.0.0.1'
port = '8181'
requestsFile = dirname(realpath(__file__)) + '/' + 'requests.txt'

def main():
	global username, password, ipAddress, port

	url = 'http://%s:%s@%s:%s/apidoc/explorer/index.html' %(username, password, ipAddress, port)
	
	driver = webdriver.Firefox()
	driver.get(url)
	driver.switch_to_alert().accept()

	try:
		WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Show/Hide')))
	except:
		print 'Timeout'
		driver.quit()
		main()

	for i in driver.find_elements_by_link_text('Show/Hide'):
		i.click()

	soup = BeautifulSoup(driver.page_source, 'html.parser')

	with open(requestsFile, 'w') as f:
		for i in soup.findAll('li', {'class': 'endpoint'}):
			f.write('#httpRequest\n')
			f.write(i.find('span', {'class': 'http_method'}).text.strip() + '\n')
			f.write(i.find('span', {'class': 'path'}).text.strip() + '\n')
			if i.find('code', {'class': 'json'}):
				f.write(i.find('code', {'class': 'json'}).text + '\n')

	driver.quit()

if __name__ == '__main__':
	main()