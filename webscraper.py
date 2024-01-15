# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import json

mozilla_html_elements_reference = "https://developer.mozilla.org/en-US/docs/Web/HTML/Element"

def fetch_treasure() -> dict:
    '''Fetches all html elements and descriptions from 
    each table elem on mozilla's html docs page'''
    treasure = {}
    webpage = requests.get(mozilla_html_elements_reference)

    if webpage.status_code != 200:
        print("Error fetching webpage")
        return

    soup = BeautifulSoup(webpage.text, 'html.parser')
    tables = soup.find_all('table')

    for table in tables:

        table_rows = table.find_all('tr')

        for row in table_rows:

            table_data = row.find_all('td')

            if len(table_data) != 2:
                print("Irregular table data:", table_data)
                continue

            elem = table_data[0]
            description = table_data[1]

            if elem and description:
                treasure[elem.text] = description.text

    return treasure
    
def read_treasure() -> dict:
    '''Reads the treasure dictionary from memory, returns {} if not found'''
    try:
        with open('treasure.json', 'r') as file:
            treasure = json.load(file)
            return treasure

    except FileNotFoundError:
       return {}

def write_treasure(treasure: dict):
    '''Writes the treasure dictionary to memory'''
    with open('treasure.json', 'w') as file:
        json.dump(treasure, file)

def main():
    treasure = read_treasure()

    if not treasure:
        print("Treasure not found, fetching...")
        treasure = fetch_treasure()
        write_treasure(treasure)

    print(treasure)

if __name__ == '__main__':
    main()