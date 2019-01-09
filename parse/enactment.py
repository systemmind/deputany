#! /usr/bin/env python
# -*- coding: utf-8 -*-
#import argparse
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import re
import json
import csv
from strings import *


class Enactment(object):
    def __init__(self, driver):
        self._driver = driver

    def sync(self, test):
        self._driver.get(STR_ENACTMENTS_URL)
        next_page_exist = True
        self._enactments = []
        while next_page_exist:
            list_archve = self._driver.find_element(By.ID, STR_LIST_ARCHIVE)
            dates = list_archve.find_elements(By.CLASS_NAME, STR_DATE)
            descriptions = list_archve.find_elements(By.CLASS_NAME, STR_NEWS_ITEM)

            for raw_date, descr in zip(dates, descriptions):
                date = self.date_time(raw_date.text)
                descript_result = self.description_result(descr.text)
                details = descr.find_element(By.CLASS_NAME, STR_DETAILS)
                href = details.find_element(By.TAG_NAME, 'a').get_attribute(STR_HREF)
                self._enactments.append([href, date[0], date[1], descript_result[0], descript_result[1]])

            try:
                if test:
                    break
                page_next = self._driver.find_element(By.CLASS_NAME, STR_PAGE_NEXT)
                actions = ActionChains(self._driver)
                actions.move_to_element(page_next).perform()
                page_next.click()

            except NoSuchElementException as err:
                print(err)
                next_page_exist = False

    def save(self):
        with open(STR_ENACTMENTS_CSV, 'w') as file:
            writer = csv.writer(file)
            for enactment in self._enactments:
                writer.writerow(enactment)

    def date_time(self, text):
        mounths = {u" СІЧНЯ ": "01",
                   u" ЛЮТОГО ": "02",
                   u" БЕРЕЗНЯ ": "03",
                   u" КВІТНЯ ": "04",
                   u" ТРАВНЯ ": "05",
                   u" ЧЕРВНЯ ": "06",
                   u" ЛИПНЯ ": "07",
                   u" СЕРПНЯ ": "08",
                   u" ВЕРЕСНЯ ": "09",
                   u" ЖОВТНЯ ": "10",
                   u" ЛИСТОПАДА ": "11",
                   u" ГРУДНЯ ": "12"}

        date_str = re.search(u'^(.*)\d{4}', text).group(0)
        list_date = date_str.split(" ")
        mounth = re.search(r'\s\D{1,}', date_str).group(0)
        mounth = mounths[mounth]
        time = re.search(r'\d+:\d+', text).group(0)
        day_mounth_year = list_date[0]+"."+mounth+"."+list_date[2]

        return [day_mounth_year, time]

    def description_result(self, text):
        try:
            split_text = text.split("\n")
            description = split_text[0].encode("utf-8")
            result = re.search(r'Рішення(.*)рийнято', split_text[2].encode("utf-8")).group(0)
            return [description, result]
        except IndexError as err:
            return [description, ""]
