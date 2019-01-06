#! /usr/bin/env python
# -*- coding: utf-8 -*-
#import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from enactment import Enactment
import re
import csv
import hashlib

class Votes (object):
    def __init__(self, driver):
        self._driver = driver

    def sync(self, url, start_date, before_date):
        self._driver.get(url)
        self._file_name = re.search(r'\d+', url).group(0)
        try:
            self._driver.find_element_by_link_text("Голосування депутата").click()
            date_input = self._driver.find_element(By.ID, "Data1")
            date_input.clear()
            date_input.send_keys(start_date)
            if before_date is not None:
                date_input = self._driver.find_element(By.ID, "Data2")
                date_input.clear()
                date_input.send_keys(before_date)

            self._driver.find_element(By.CLASS_NAME, 'search_button1').click()
            try:
                self._driver.find_element(By.ID, "s0").click()
            except NoSuchElementException as err:
                pass

            available = False
            self._votes = []
            self._enactments_urls = []
            while available == False:
                try:
                    time.sleep(1)
                    print("wait")
                    pd = self._driver.find_element(By.CLASS_NAME,'pd')
                    block_pd_list = pd.find_elements(By.CLASS_NAME,'block_pd')

                    for element in block_pd_list:
                        zname = element.find_element(By.CLASS_NAME, 'zname')
                        href = zname.find_element(By.TAG_NAME, 'a').get_attribute('href')
                        rezult = element.find_element(By.CLASS_NAME, 'zrez').text
                        self._votes.append([url, href.encode("utf-8"), rezult.encode("utf-8")])
                        self._enactments_urls.append(href.encode("utf-8"))
                        print(str(href)+"  "+ rezult)
                    
                    available = True

                except StaleElementReferenceException:
                    pass

                except NoSuchElementException:
                    pass
        except NoSuchElementException as err:
            print(str(err))
            self._driver.quit()

    def save(self):
        enactment = Enactment(self._driver)
        with open(self._file_name + '_enactment.csv', 'w') as file:
            writer = csv.writer(file)
            for href in self._enactments_urls:
                writer.writerow(enactment.sync(href))

        with open(self._file_name + '.csv', 'w') as file:
            writer = csv.writer(file)
            for vote in self._votes:
                writer.writerow(vote)

            return (self._file_name + '_enactment.csv', hashlib.md5(open(self._file_name + '_enactment.csv', 'rb').read()).hexdigest())
