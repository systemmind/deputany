#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time
from selenium import webdriver
from enactment import Enactment
from votes import Votes
from persons import Persons
import re
import csv
import os
import platform
import os.path
from strings import *

if platform.system() == "Linux":
    driver = webdriver.Firefox()
else:
    driver = webdriver.Chrome()
        

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", help="select votes from  start date", type=str, default="27.11.14")
parser.add_argument("-b", "--before", help="select votes before date", type=str, default=None)
parser.add_argument("-t", "--test", help="argument for testing", type=bool, default=False)

args = parser.parse_args()
if not os.path.isfile(STR_ENACTMENTS_CSV): 
    enactment = Enactment(driver)
    enactment.sync(args.test)
    enactment.save()

persons = Persons()
deputats = persons.sync(driver)
votes = Votes(driver)
for deputat in deputats:
    votes.sync(deputat[0], args.start, args.before)

persons.save()
driver.quit()
