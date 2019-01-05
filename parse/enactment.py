#! /usr/bin/env python
# -*- coding: utf-8 -*-
#import argparse
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import re
import json
import csv

class Enactment(object):
    def __init__(self, driver):
        self._driver = driver

    def sync(self, url):
        self._driver.get(url)
        self._file_name = re.search(r'\d{5}', url).group(0)
        head_gol = self._driver.find_element(By.CLASS_NAME, "head_gol")
        list_text = head_gol.text.split("\n")
        description = list_text[0]
        date_time = list_text[1]
        date = re.search(r'\d+\.\d+\.\d+', date_time).group(0)
        time = re.search(r'\d+:\d+', date_time).group(0)
        result = list_text[3]
        print (url.encode("utf-8")+" "+date.encode("utf-8")+" "+time.encode("utf-8")+" "+ result.encode("utf-8"))
        return [url.encode("utf-8"), date.encode("utf-8"), time.encode("utf-8"), description.encode("utf-8"), result.encode("utf-8")]
