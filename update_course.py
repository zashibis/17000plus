# -*- coding: utf-8 -*- 

import io
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException

f = io.open("17000+words.txt", 'r', encoding='utf8')
firefox_config = u"c:/Users/Name/AppData/Roaming/Mozilla/Firefox/Profiles/95a6eyng.default"
url = "http://www.memrise.com/course/1128552/17000-sovremennykh-populiarnykh-slov/edit/"

words = []
for line in f:
	words.append(line.split("	"))

fp = webdriver.FirefoxProfile(firefox_config)
browser = webdriver.Firefox(fp)
browser.set_page_load_timeout(60)

while 1:
	try:
		browser.get(url)
		break
	except TimeoutException:
		browser.close()
		browser = webdriver.Firefox(fp)
		browser.set_page_load_timeout(60)
		continue
time.sleep(5)

level_number = 180
start_level = 1
update_sounds = False

for n in range(start_level-1, level_number):
	print "********************************************************************"
	print n + 1
	# Show lesson
	browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").click()
	i = 0
	while 1:
		i = i + 1
		if i > 30:
			browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").send_keys(u'\ue013')
			browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").send_keys(u'\ue013')
			browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").click()
			time.sleep(1)
			i = 0
		try:
			if browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("level-things").is_displayed():
				break
		except NoSuchElementException:
			time.sleep(1)
		except StaleElementReferenceException:
			time.sleep(1)
	time.sleep(3)
	
	# Start working with the lesson
	things = browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("level-things").find_element_by_class_name("things").find_elements_by_class_name("thing")
	for row in things:
		columns = row.find_elements_by_tag_name("td")

		# Looking for the word in the source
		word = columns[1].find_element_by_class_name("text").text
		print word
		word_found = False
		for item in words:
			if item[1] == word:
				word_found = True
				
				#calculate meaning
				meaning = ""
				if item[3] != "":
					meaning = item[3] + " "
				meaning = meaning + item[4]				
				syn_list = item[5].split(", ")
				if syn_list[0] != "":
					meaning = meaning + u" (не: "
					for syn in syn_list:
						if len(meaning + syn) > 150:
							break
						meaning = meaning + syn + ", "
					meaning = meaning[:-2]
					meaning = meaning + ")"
				
				#update meaning if it's differ
				if columns[2].find_element_by_class_name("text").text != meaning:
					while 1:
						try:
							columns[2].find_element_by_class_name("text").click()
							break
						except WebDriverException:
							columns[2].send_keys(u'\ue013')
					time.sleep(1)
					i = 0
					while 1:
						i = i + 1
						if i > 3:
							columns[2].find_element_by_class_name("text").click()
							time.sleep(1)
							i = 0
						try:
							columns[2].find_element_by_tag_name("input").clear()
							break
						except NoSuchElementException:
							time.sleep(1)
					columns[2].find_element_by_tag_name("input").send_keys(meaning)
					time.sleep(2)

				#update pronunciation
				if columns[4].find_element_by_class_name("text").text != item[2]:
					columns[4].find_element_by_class_name("text").click()
					time.sleep(1)
					i = 0
					while 1:
						i = i + 1
						if i > 3:
							columns[4].find_element_by_class_name("text").click()
							time.sleep(1)
							i = 0
						try:
							columns[4].find_element_by_tag_name("input").clear()
							break
						except NoSuchElementException:
							time.sleep(1)
					columns[4].find_element_by_tag_name("input").send_keys(item[2])
					time.sleep(2)
				
				#update sounds
				if update_sounds:
					#delete old sound
					while 1:
						try:
							columns[3].find_element_by_class_name("dropdown-toggle").click()
							break
						except WebDriverException:
							columns[3].send_keys(u'\ue013')
					time.sleep(1)
					i = 0
					while 1:
						i = i + 1
						if i > 3:
							columns[3].find_element_by_class_name("dropdown-toggle").click()
							time.sleep(1)
							i = 0
						try:
							if columns[3].find_element_by_class_name("ico-trash").is_displayed():
								break
						except NoSuchElementException:
							time.sleep(1)
					
					while 1:
						try:
							columns[3].find_element_by_class_name("ico-trash").click()
							break
						except WebDriverException:
							columns[3].send_keys(u'\ue013')
							time.sleep(1)

					time.sleep(1)
					i = 0
					while 1:
						i = i + 1
						if i > 3:
							try:
								row.find_elements_by_tag_name("td")[3].find_element_by_class_name("ico-trash").click()
							except NoSuchElementException:
								break
							except StaleElementReferenceException:
								break
							time.sleep(1)
							i = 0
						try:
							row.find_elements_by_tag_name("td")[3].find_element_by_class_name("ico-trash")
							time.sleep(1)
						except NoSuchElementException:
							break
						except StaleElementReferenceException:
							break
					#upload new sound
					time.sleep(1)
					row.find_elements_by_tag_name("td")[3].find_element_by_class_name("add_thing_file").clear()
					file_name = "c:\\Temp\\update_course\\mp3\\" + word + "_us_uk.mp3"
					row.find_elements_by_tag_name("td")[3].find_element_by_class_name("add_thing_file").send_keys(file_name)
					time.sleep(1)
					while 1:
						try:
							row.find_elements_by_tag_name("td")[3].find_element_by_class_name("ico-trash")
							time.sleep(1)
							break
						except NoSuchElementException:
							time.sleep(1)
						except StaleElementReferenceException:
							time.sleep(1)
					
		#delete word if it's not found in the source
		if word_found == False:
			while 1:
				try:
					columns[0].find_element_by_class_name("ico-close").click()
					break
				except WebDriverException:
					columns[0].find_element_by_class_name("ico-close").send_keys(u'\ue013')
			time.sleep(1)
			i = 0
			while 1:
				i = i + 1
				if i > 5:
					columns[0].find_element_by_class_name("ico-close").click()
					time.sleep(1)
					i = 0
				try:
					browser.find_element_by_link_text("Yes").click()
					break
				except NoSuchElementException:
					time.sleep(1)
			time.sleep(5)
	
	time.sleep(3)
	#hide lesson
	browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").send_keys(u'\ue013')
	time.sleep(3)
	#button must be on the screen
	while 1:
		try:
			browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").click()
			break
		except WebDriverException:
			browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").send_keys(u'\ue013')
			time.sleep(1)
	i = 0
	while 1:
		i = i + 1
		if i > 5:
			browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("show-hide").click()
			time.sleep(1)
			i = 0
		try:
			if not browser.find_element_by_id("levels").find_elements_by_class_name("level")[n].find_element_by_class_name("level-things").is_displayed():
				break
		except NoSuchElementException:
			time.sleep(1)
	time.sleep(3)
	