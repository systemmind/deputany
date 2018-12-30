import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

driver = webdriver.Chrome("chromedriver.exe")
driver.implicitly_wait(10)
driver.get('http://w1.c1.rada.gov.ua/pls/site2/p_deputat_list')
all_content = driver.find_element(By.XPATH, './/*[@id="btnAllMPS"]')
all_content.click()
deps_list = driver.find_element(By.XPATH, './/*[@id="search_results"]/ul')
elements = deps_list.find_elements_by_tag_name("li")
names_references = {}

for element in elements:
    title = element.find_element_by_class_name("title")
    href = title.find_element_by_css_selector('a').get_attribute('href')
    names_references.update({title.text.encode("utf-8"): href.encode("utf-8")})
    print(title.text.encode("utf-8") + " : " + href.encode("utf-8"))

deputans = {"deputans": names_references}
with open("deputans.json", 'w') as outfile:
    json.dump(deputans, outfile)

driver.quit()
