# Link for Google sheets
# https://docs.google.com/spreadsheets/d/1jlfiwJWA9vMlT9f-_tzIEOpvGNdn23GGS32zTZgA1HM/edit?resourcekey#gid=1514182019

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_driver_path = r"C:\Users\Zemmente\Desktop\chromedriver"
driver = webdriver.Chrome(options=chrome_options)

URL = 'https://www.njuskalo.hr/prodaja-stanova/dugo-selo?price%5Bmax%5D=150000&buildingInfo%5Bnew-building%5D=1&parkingSpotType%5Bparking-garage%5D=1&parkingSpotType%5Bgarage-spot%5D=1&parkingSpotType%5Bparking-outdoor-covered%5D=1'

header = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
  "Accept-Language": "hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(URL, headers=header)

web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')

# Prices
prices_dirty = soup.select('div > ul > li > strong')
prices_list_clean = [price.getText().split()[0] for price in prices_dirty]


# Description
description_dirty = soup.select('li > article > div > div')
description_list = [' '.join(description.getText().split()) for description in description_dirty]
description_list_clean = list(filter(None, description_list))


# Links
links = soup.select('div > ul > li > article > h3 > a')
links_list = ['www.njuskalo.hr' + link.get('href') for link in links]
min_length = min(len(prices_list_clean), len(description_list_clean))
# Make sure the links_list is equal to length of the other two lists
links_list = links_list[:min_length]


# SELENIUM DRIVER
all_info = zip(prices_list_clean, description_list_clean, links_list)

driver.get('https://docs.google.com/forms/d/1gLFzU3rZ4J7qA4bvAR7wxYUSd4UPfu1onqQ_wh3F6v4/edit')

for info in all_info:
    # FIRST FIELD
    first_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(1)
    first_field.click()
    first_field.send_keys(info[0])

    # SECOND FIELD
    second_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    second_field.click()
    second_field.send_keys(info[1])

    # THIRD FIELD
    third_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    third_field.click()
    third_field.send_keys(info[2])

    # SUBMIT BUTTON
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()

    # ANOTHER RESPONSE BUTTON
    time.sleep(1)
    another_response_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    another_response_button.click()
