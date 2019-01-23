#! /usr/bin/env python
# -*- coding: utf-8 -*-
#import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from enactment import Enactment
import re
import csv
import hashlib
import errno
import os


class Votes (object):
    def __init__(self, file_name, deputats, from_date, to_date):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        self._file_name = file_name
        self._deputats = deputats
        self._driver = webdriver.Chrome(chrome_options=chrome_options)
        self._from_date = from_date
        self._to_date = to_date
        self._votes = []

    def sync(self, url):
        self._driver.get(url)
        try:
            self._driver.find_element_by_link_text("Голосування депутата").click()
            date_input = self._driver.find_element(By.ID, "Data1")
            date_input.clear()
            date_input.send_keys(self._from_date)

            if self._to_date is not None:
                date_input = self._driver.find_element(By.ID, "Data2")
                date_input.clear()
                date_input.send_keys(self._to_date)

            self._driver.find_element(By.CLASS_NAME, 'search_button1').click()
            try:
                wait = WebDriverWait(self._driver, 1)
                element = wait.until(EC.presence_of_element_located((By.ID, "s0")))
                element.click()
            except Exception as err:
                pass

            wait = WebDriverWait(self._driver, 300)
            block_pd_list = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "block_pd")))

            for element in block_pd_list:
                text = element.text.split("\n")
                print(text[0].decode("utf-8"))
                self._votes.append(u"'"+url+u"'\t'"+element.find_element(By.TAG_NAME, 'a').get_attribute('href')+u"'\t'"+text[2]+u"'\n")

        except NoSuchElementException as err:
            print(str(err))
            self._driver.quit()

    def sync_all(self):
        for i in range(len(self._deputats)):
            try:
                print("deputat " + str(i))
                self.sync(self._deputats[i][0])
            except Exception as err:
                    print("sync_all error")
                    print(str(err))
                    i -= 1
                    continue

        self.save()
        self._driver.quit()

    def save(self):
        with open(self._file_name + '.csv', 'w') as file:
            for vote in self._votes:
                file.write(vote.encode("utf-8"))

    @staticmethod
    def merge_files(amount):
        data = []
        for i in range(amount):
            file_name = str(i)+'.csv'
            if os.path.isfile(file_name):
                with open(file_name, 'r') as file:
                    for line in file:
                        data.append(line)

        with open('votes.csv', 'w') as file:
            for line in data:
                file.write(line)
        
        for i in range(amount):
            file_name = str(i)+'.csv'
            if os.path.isfile(file_name):
                os.remove(file_name)
