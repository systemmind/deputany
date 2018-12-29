import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("chromedriver.exe")
driver.implicitly_wait(10)
driver.get('http://w1.c1.rada.gov.ua/pls/site2/p_deputat_list')

all_content = driver.find_element_by_id("content-all")
information_block = all_content.find_element_by_class_name("information_block")
information_block_ins = information_block.find_element_by_class_name("information_block_ins")
info_box = information_block_ins.find_element_by_class_name("info_box")
information_block_ins = information_block.find_element_by_class_name("information_block_ins")
coll_half = information_block_ins.find_element_by_class_name("col-half")
links = coll_half.find_element_by_class_name("links")
search_type = links.find_elements_by_tag_name("li")
all_deps = search_type[0].find_element_by_id("btnAllMPS")
all_deps.click()
search_result = information_block_ins.find_element_by_id("search_results")
deps_list = search_result.find_element_by_tag_name('ul')
elements = deps_list.find_elements_by_tag_name("li")
with open("deputans.txt", 'w') as outfile:
    for element in elements:
        title = element.find_element_by_class_name("title")
        href = title.find_element_by_css_selector('a').get_attribute('href')
        outfile.write(title.text.encode("utf-8") + " : " + href.encode("utf-8"))
        print(title.text.encode("utf-8") + " : " + href.encode("utf-8"))

driver.quit()
