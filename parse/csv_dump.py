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

class CheckSummError(Exception):
    def __init__(self, message):
        super(CheckSummError, self).__init__(message)
if platform.system() == "Linux":
    driver = webdriver.Firefox()
else:
    driver = webdriver.Chrome()
        

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--start", help="select votes from  start date", type=str, default="27.11.14")
parser.add_argument("-b", "--before", help="select votes before date", type=str, default=None)
args = parser.parse_args()
persons = Persons()
deputats = persons.sync(driver)
votes = Votes(driver)
hashes = []
try:
    for i in range(5):
        votes.sync(deputats[i][0], args.start, args.before)
        hashes.append(votes.save())
        if len(hashes) == 1:
            continue
        else:
            print(hashes[0][1])
            print(hashes[1][1])
            if hashes[0][1] == hashes[1][1]:
                os.remove(hashes[1][0])
                hashes.remove(hashes[1])
                print("hashes *enactment.csv file is equal")
                continue
            else:
                print("hashes *enactment.csv file is not equal")
                raise CheckSummError("hash summ enactment.csv files is not equal")
except CheckSummError as err:
    persons.save()
    print(err)
    driver.quit()

driver.quit()
