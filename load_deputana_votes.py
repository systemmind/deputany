import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import re
import json

driver = webdriver.Chrome("chromedriver.exe")
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="deputana profile url", type=str)
parser.add_argument("-d", "--date", help="slect votes from date", type=str, default="27.11.14")
args = parser.parse_args()
file_name = re.findall(r'\d+',args.url)[0]

driver.implicitly_wait(10)
driver.get(args.url)
try:
    driver.find_element(By.XPATH, './/*[@id="mp_content"]/div/div[4]/a[1]').click()
    date_input = driver.find_element(By.XPATH, './/*[@id="Data1"]')
    date_input.clear()
    date_input.send_keys(args.date)
    driver.find_element(By.XPATH, './/*[@id="PlsqlBody"]/center/form/center/input[2]').click()
    driver.find_element(By.XPATH, './/*[@id="s0"]').click()
    time.sleep(5)
    pd = driver.find_element(By.XPATH,'.//*[@id="list_g"]/ul')
    li_list = pd.find_elements(By.XPATH, './/li/div[@class="block_pd"]')
    dict_votes = {}

    for li in li_list:
        text = li.find_element_by_class_name("zname").text
        rezult = li.find_element_by_class_name("zrez").text
        dict_votes.update({text: rezult})
        print(text)

except NoSuchElementException as err:
    print(str(err))
    driver.quit()

deputana_votes = {"laws": dict_votes}
with open(file_name + ".json", 'w') as fout:
    json.dump(deputana_votes, fout)

driver.quit()
