from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import random


URL = "https://www.zillow.com/san-francisco-ca/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.52499667529297%2C%22east%22%3A-122.34166232470703%2C%22south%22%3A37.662044543503555%2C%22north%22%3A37.88836615784793%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
]

service = Service()
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={random.choice(user_agents)}")
driver = webdriver.Chrome(service=service, options=options)

driver.get(URL)
time.sleep(random.uniform(3, 5))

scroll_increment = 0
while scroll_increment < 600: 
    driver.execute_script(f"window.scrollTo(0, {scroll_increment * 10});")
    time.sleep(random.uniform(1, 2))
    scroll_increment += 100

web_page = driver.page_source
driver.quit()

soup = BeautifulSoup(web_page, 'lxml')


#---------------- Prices ----------------#
prices_dirty = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")
prices_list_clean = [price.getText().split()[0] for price in prices_dirty if price.getText().startswith('$')]
print(prices_list_clean)

#---------------- Bedrooms and bathrooms ----------------#
quantity_dirty = soup.find_all("ul", class_="StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 eYPFID")
quantity_list_clean = [
    " ".join(
        q.getText(strip=True)
        for q in quantity.select("li")
        if not q.getText().startswith("--")
    )
    for quantity in quantity_dirty
]
print(quantity_list_clean)

#---------------- Adresses ----------------#
adresses_dirty = soup.find_all("address")
adresses_list_clean = [adress.getText() for adress in adresses_dirty]
print(adresses_list_clean)






# ------------------------------------------- ONLY BEAUTIFUL SOUP ------------------------------------------- #

# import requests
# from bs4 import BeautifulSoup

# URL = "https://www.zillow.com/san-francisco-ca/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.52499667529297%2C%22east%22%3A-122.34166232470703%2C%22south%22%3A37.662044543503555%2C%22north%22%3A37.88836615784793%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

# header = {
#   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
#   "Accept-Language": "hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7"
# }

# response = requests.get(URL, headers=header)

# web_page = response.text

# soup = BeautifulSoup(web_page, 'lxml')

# #-------------------------------------------------------- Prices
# #prices_dirty = soup.select("div > ul > li > div > div >article > div > div > div > div > span")
# #prices_dirty = soup.select("span.PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")
# prices_dirty = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr")
# prices_list_clean = [price.getText().split()[0] for price in prices_dirty if price.getText().startswith('$')]
# print(prices_list_clean)


# # Bedrooms and bathrooms
# quantity_dirty = soup.find_all("ul", class_="StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 eYPFID")
# quantity_list_clean = [
#     " ".join(
#         q.getText(strip=True)
#         for q in quantity.select("li")
#         if not q.getText().startswith("--")
#     )
#     for quantity in quantity_dirty
# ]
# print(quantity_list_clean)



# # Adresses
# #adresses_dirty = soup.select('div > div > article > div > div > a')
# adresses_dirty = soup.find_all("address")
# adresses_list_clean = [adress.getText() for adress in adresses_dirty]
# print(adresses_list_clean)
