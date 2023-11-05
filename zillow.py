import requests
from bs4 import BeautifulSoup
import gspread

URK = "https://shorturl.at/afgm8"
#URL = "https://www.zillow.com/san-francisco-ca/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.52499667529297%2C%22east%22%3A-122.34166232470703%2C%22south%22%3A37.662044543503555%2C%22north%22%3A37.88836615784793%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22days%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

header = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
  "Accept-Language": "hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(URL, headers=header)

web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')

# Prices
prices_dirty = soup.select('div > ul > li > div > div >article > div > div > div > div > span')
prices_list_clean = [price.getText().split()[0] for price in prices_dirty if price.getText().startswith('$')]
#print(prices_list_clean)


# Bedrooms and bathrooms
quantity_dirty = soup.select('div > div > article > div > div > div > ul > li')
quantity_list_clean = [quantity.getText() for quantity in quantity_dirty if not quantity.getText().startswith('--')]
chunk_size = 3
quantity_sublists = [quantity_list_clean[i:i + chunk_size] for i in range(0, len(quantity_list_clean), chunk_size)]
#print(quantity_list_clean)
#print(quantity_sublists)


# Adresses
adresses_dirty = soup.select('div > div > article > div > div > a')
adresses_list_clean = [adress.getText() for adress in adresses_dirty]
print(adresses_list_clean)
