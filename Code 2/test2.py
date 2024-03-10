from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

def Selenium_extractor(location, search_query):
    filename = f"data_{location}_{search_query}"
    link = f"https://www.google.com/maps/search/{search_query}+in+{location}"

    browser = webdriver.Chrome()
    record = []
    e = []
    le = 0

    browser.get(link)
    time.sleep(10)

    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

    while len(a) < 1000:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()
        time.sleep(2)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

        if len(a) == var:
            le+=1
            if le > 20:
                break
        else:
            le = 0

    for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 100).perform()
        action.move_to_element(a[i]).perform()
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            Name_Html = soup.findAll('h1', {"class": "DUwDvf fontHeadlineLarge"})

            name = Name_Html[0].text
            if name not in e:
                e.append(name)
                divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium"})
                for j in range(len(divs)):
                    if str(divs[j].text)[0] == "+":
                        phone = divs[j].text

                Address_Html= divs[0]
                address=Address_Html.text
                try:
                    for z in range(len(divs)):
                        if str(divs[z].text)[-4] == "." or str(divs[z].text)[-3] == ".":
                            website = divs[z].text
                except:
                    website="Not available"
                print([name,phone,address,website])
                record.append((name,phone,address,website))
                df=pd.DataFrame(record,columns=['Name','Phone number','Address','Website'])  # writing data to the file
                df.to_csv(filename + '.csv',index=False,encoding='utf-8')
        except:
            print("error")
            continue

    browser.quit()

# Prompt user for location and search query
location = input("Enter the location: ")
search_query = input("Enter the search query: ")

Selenium_extractor(location, search_query)
