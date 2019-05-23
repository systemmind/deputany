#! /usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from enactment import Enactment
from votes import Votes
from persons import Persons
import re
import csv
import os
import platform
import os.path
import threading
from strings import *


def devide_array(lst, n):
    return [lst[i::n] for i in xrange(n)]

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fromd", help="select votes from date", type=str, default="27.11.2014")
parser.add_argument("-t", "--tod", help="select votes to date", type=str, default="22.12.2018")
parser.add_argument("--deputats", help="argument for sync dpeputats", action='store_const', const='True', default=False)
parser.add_argument("--enactments", help="argument for sync enactments", action='store_const', const='True', default=False)
parser.add_argument("--threads", help="argument for amount of threads for sync enactments", type=int, default=4)
args = parser.parse_args()

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(chrome_options=chrome_options)
deputats = None
date_from = datetime.datetime.strptime(args.fromd, "%d.%m.%Y")
date_to = datetime.datetime.strptime(args.tod, "%d.%m.%Y")


if args.deputats:
    print('--deputats = True: sync deputats')
    persons = Persons()
    deputats = persons.sync(driver)
    persons.save()
else:
    print('--deputats = False: load deputats')
    persons = Persons()
    deputats = persons.load()

if args.enactments:
    print('--enactment not None: sync enactments')
    enactment = Enactment(driver)
    enactment.sync(date_from, date_to)
    enactment.save()

threads_amount = args.threads
list_deps = devide_array(deputats, threads_amount)
list_Votes = []
pool_threads = []

for i in range(threads_amount):
    list_Votes.append(Votes(str(i), list_deps[i], args.fromd, args.tod))
    pool_threads.append(threading.Thread(target=list_Votes[i].sync_all))
    pool_threads[i].start()

for thread in pool_threads:
    thread.join()


Votes.merge_files(threads_amount)
driver.quit()
