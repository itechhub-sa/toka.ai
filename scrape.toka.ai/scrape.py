# The standard library modules
import os
import sys

# The wget module
import wget

# The BeautifulSoup module
from bs4 import BeautifulSoup

# The selenium module
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


#driver = webdriver.Chrome('/home/asive/Documents/projects/toka/chromedriver') 
driver = webdriver.PhantomJS('phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
                             service_args=['--ignore-ssl-errors=true'])
driver.get("https://www.parliament.gov.za/legislation") # load the web page

year_select = driver.find_element_by_id('billYear')
years_map = map(lambda elem: elem.get_attribute('value'),
                year_select.find_elements_by_tag_name('option'))
years_list = list(years_map)

# Change year
#driver.implicitly_wait(60)
driver.find_element_by_xpath("//select[@id='billYear']/option[text()='"+ '2012' + "']").click()

table = driver.find_element_by_tag_name('table')
td = table.find_elements_by_tag_name('td')[2].text

print("TD: ", td.startswith('2017'))

#select = Select(year_select)
#selected_option = select.first_selected_option
#print("Selected option: ", selected_option.text)

src = driver.page_source

# initialize the parser and parse the source "src"
bs = BeautifulSoup(src, "lxml") 

for link in bs.find_all("a"):
    content = link.get("")
    href = link.get("href")

    if href is not None:
        if href.endswith("pdf"):
            pass
            #print("Text: ", link.contents[0])
            #print("Link: ", href)
