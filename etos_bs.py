import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.maximize_window()

#get method to hit url on  browser
driver.get("https://www.etos.nl/")

driver.find_element("xpath", '//*[@name="sluit de cookiebar"]').click()

driver.find_element("xpath","//button[@id='category-1']").click()

items_list = driver.find_elements("xpath", "//*[@class='main-menu__item-button']")
category_url_list = []
for items in items_list:
    category_url_list.append(items.get_attribute('href'))

product_link_with_roundel = []

for url in category_url_list:
    time.sleep(5)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for i in soup.find_all("span", attrs={"class": "js-result-count"}):
        name = i.get_text()
        val = name.strip(" ").strip("\n")
        if len(val) < 4:
            name = int(name.strip(" ").strip("\n"))
        else:
            name = float(name.strip(" ").strip("\n")) * 1000

        pages = name / 24
        base_url = url + "?prefn1=isHiddenProduct&prefv1=false&start=" + str(int(pages) * 24) + "&sz=24"

        page = requests.get(base_url)
        soup = BeautifulSoup(page.text, 'html.parser')

        for i in soup.find_all("div", attrs={"class": "product product-grid__product js-grid-tile-product"}):
            name = i.get_text()
            link_product = ""
            for a in i.find_all('a', href=True):
                link_product = a['href']

            images = i.findAll('img')
            for image in images:
                if "1plus1" in image['src']:
                    print(link_product)
                    product_link_with_roundel.append(link_product)


df = pd.DataFrame(product_link_with_roundel)

df.to_csv("etos_bs.csv")
