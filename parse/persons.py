import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import csv


class Persons(object):
    def __init__(self):
        self._names_references = []

    def sync(self, driver):
        driver.implicitly_wait(5)
        driver.get('http://w1.c1.rada.gov.ua/pls/site2/p_deputat_list')
        time.sleep(1)
        all_content = driver.find_element(By.ID, 'btnAllMPS')
        all_content.click()
        deps_list = driver.find_element(By.ID, 'search_results')
        elements = deps_list.find_elements_by_tag_name("li")

        for element in elements:
            title = element.find_element_by_class_name("title")
            href = title.find_element_by_css_selector('a').get_attribute('href')
            self._names_references.append((href.encode("utf-8"), title.text.encode("utf-8")))
            print(href.encode("utf-8") + "---" + title.text.encode("utf-8"))

        return self._names_references

    def save(self):
        with open("deputats.csv", "w") as file:
            writer = csv.writer(file)
            for element in self._names_references:
                writer.writerow(element)

    def load(self):
        with open("deputats.csv", "r") as file:
            lines = file.readlines()
            for line in lines:
                list_words = line.split(",")
                self._names_references.append((list_words[0], list_words[1]))

            return self._names_references
