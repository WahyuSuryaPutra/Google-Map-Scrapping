from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def scrape_google_maps(location, search_query):
    results = []
    url = f"https://www.google.com/maps/search/{location} {search_query}"
    # Prepare chrome browser
    browser = webdriver.Chrome()
    # inject the google url into the browser
    browser.get(url)
    # wait for 5 seconds to make sure the google maps is fully loaded
    time.sleep(5)
    # scroll delay
    scroll_pause_time = 2
    # Bassically track how deep we scroll down
    last_scroll_height = 0

    while True:
        # For some reason is just got scroll to 5 locations and jump back to beginning
        for _ in range(5):
            browser.execute_script(f"window.scrollBy(0, 500)")
            time.sleep(scroll_pause_time / 5)

        #  Collect data
        malls = browser.find_elements(By.CLASS_NAME, "hfpxzc")
        for mall in malls:
            try:
                # click to open the more details about the location
                actions = ActionChains(browser)
                actions.move_to_element(mall).click().perform()
                time.sleep(2)

                # fix for stale refences error and
                # get the location data like name,rating and address
                try:
                    name = browser.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text
                except (NoSuchElementException, StaleElementReferenceException):
                    name = ""

                try:
                    rating = browser.find_element(By.CLASS_NAME, "aMPvhf-fI6EEc-KVuj8d").text
                except (NoSuchElementException, StaleElementReferenceException):
                    rating = ""

                try:
                    address = browser.find_element(By.CSS_SELECTOR, '[data-item-id="address"]').text
                except (NoSuchElementException, StaleElementReferenceException):
                    address = ""

                # append the data into results array
                results.append({
                    'name': name,
                    'rating': rating,
                    'address': address
                })

            except Exception as e:
                print(f"Error scraping individual mall: {e}")

        # keep scrolling until we can't scroll again and save how much we already scroll down
        new_scroll_height = browser.execute_script("return document.body.scrollHeight")
        if new_scroll_height == last_scroll_height:
            print("Reached the end or no new data.")
            break
        last_scroll_height = new_scroll_height

    browser.quit()
    return results

# Prompt user for location and search query
location = input("Enter the location: ")
search_query = input("Enter the search query: ")

mall_data = scrape_google_maps(location, search_query)

# Save to CSV
df = pd.DataFrame(mall_data)
df.to_csv('scrapp_mall_indo.csv', index=False)
