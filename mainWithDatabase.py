import requests
import sqlite3
import time
from bs4 import BeautifulSoup

# Create table if it doesn't exist
create_table_query = '''CREATE TABLE IF NOT EXISTS Apartments (
                        id INTEGER PRIMARY KEY,
                        price TEXT NOT NULL,
                        description TEXT NOT NULL,
                        links TEXT NOT NULL
                        );
    '''

database_name = 'Stanovi.db'

# Connect to database and create a cursor
sc = sqlite3.connect(database_name)
cursor = sc.cursor()
cursor.execute(create_table_query)


URL = 'https://www.njuskalo.hr/prodaja-stanova/dugo-selo?price%5Bmax%5D=150000&buildingInfo%5Bnew-' \
      'building%5D=1&parkingSpotType%5Bparking-garage%5D=1&parkingSpotType%5Bgarage-spot%5D=1&parkingSpotType%5Bparking-outdoor-covered%5D=1'

header = {
  "User-Agent":
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
  "Accept-Language": "hr-HR,hr;q=0.9,en-US;q=0.8,en;q=0.7"
}

response = requests.get(URL, headers=header)

web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')

# Prices of the apartments
prices_dirty = soup.select('div > ul > li > strong')
prices_list_clean = [price.getText().split()[0] for price in prices_dirty]


# Short description
description_dirty = soup.select('li > article > div > div')
description_list = [' '.join(description.getText().split()) for description in description_dirty]
description_list_clean = list(filter(None, description_list))


# Links
links = soup.select('div > ul > li > article > h3 > a')
links_list = ['www.njuskalo.hr' + link.get('href') for link in links]
min_length = min(len(prices_list_clean), len(description_list_clean))
links_list = links_list[:min_length]


all_info = zip(prices_list_clean, description_list_clean, links_list)

# Delete data from before
cursor.execute('DELETE FROM Apartments')

# Add new updated data
for price, description, link in all_info:
    cursor.executemany('INSERT INTO Apartments(price, description, links) VALUES (?,?,?)', all_info)

sc.commit()

print('Successfully updated.')

if sc:
    cursor.close()
    sc.close()
