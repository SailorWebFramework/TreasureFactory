from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import json
import time

TREASURE = "tailwind.json"
TOTAL_CLASSES = 1874 # as of 02-11-2024

class TailwindScraper:

    def __init__(self):
        self.tailwind_class_list = "https://tailwind.build/classes"
        self.tailwind_translations = "https://tailwind-to-css.vercel.app/"
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.treasure = {}

    def fetch_treasure(self):
        '''Fetches all tailwind css classes and descriptions'''
        self.driver.get(self.tailwind_class_list)
        categories = self.driver.find_elements(By.CSS_SELECTOR, "div.w-full.mb-6")

        for category in categories:

            classes = category.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.w-full")
            links = classes.find_elements(By.TAG_NAME, "a") # every class has a link to its own page

            for l in links:

                class_name = l.text
                if class_name in self.treasure and self.treasure[class_name] != "error fetching description": 
                    print(f"Skipping {class_name}")
                    continue # skip if already fetched
                self.treasure[class_name] = "error fetching description" # placeholder

                l.click()
                time.sleep(1) # wait for the page to load
                try:
                    # Wait for the specific element to be present
                    desc = self.driver.find_element(By.CSS_SELECTOR, "code.language-css")
                    self.treasure[class_name] = desc.text
                except NoSuchElementException:
                    print(f"Error fetching {class_name}")
                    pass

                self.write_treasure(self.treasure)
                self.driver.back()

    def translate_treasure(self):
        '''Translates the tailwind classes to css (if fetch failed)'''
        self.driver.get(self.tailwind_translations)
        time.sleep(3)
        text_inputs = self.driver.find_elements(By.TAG_NAME, "textarea")
        input_elem = text_inputs[0]
        output_elem = text_inputs[1]

        for k, v in self.treasure.items():
            if v == "error fetching description" or "{ }" in v:
                input_elem.clear()
                input_elem.send_keys(k.replace(".", ""))
                time.sleep(1)
                output = output_elem.text
                print(f"Translated {k} to {output}")
                self.treasure[k] = k + " { " + output + " }"
                self.write_treasure(self.treasure)
    
    def quit(self):
        self.driver.quit()

    def write_treasure(self, treasure: dict, name: str = TREASURE):
        '''Writes the treasure dictionary to memory'''
        with open(name, 'w') as file:
            json.dump(treasure, file)
    
    def read_treasure(self, name: str = TREASURE):
        '''Reads the treasure dictionary from memory'''
        try:
            with open(name, 'r') as file:
                self.treasure = json.load(file)

        except FileNotFoundError:
           print("Treasure not found")

    def main(self):
        print("Fetching treasure")
        self.read_treasure()
        print("total classes:", len(self.treasure))
        # treasure = self.fetch_treasure()
        treasure = self.translate_treasure()
        # self.write_treasure(treasure, "treasure_tailwind.json")
        print("Finished fetching treasure")
        self.quit()
       

if __name__ == "__main__":
    scraper = TailwindScraper()
    scraper.main()