import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.maximize_window()

# get method to hit url on  browser
driver.get("https://www.etos.nl/")

driver.find_element("xpath", '//*[@name="sluit de cookiebar"]').click()

driver.find_element("xpath", "//button[@id='category-1']").click()

items_list = driver.find_elements("xpath", "//*[@class='main-menu__item-button']")
category_url_list = []
for items in items_list:
    category_url_list.append(items.get_attribute('href'))

list_url = []

for category_url in category_url_list:
    time.sleep(5)
    driver.get(category_url)

    load_more_btn = "//*[@class='c-button--primary button--icon button--icon-right plp-next-btn js-search-loadmore-btn']"
    i = 0
    loadingButton = WebDriverWait(driver, 100).until(ec.presence_of_all_elements_located((By.XPATH, "//*[@class='c-button--primary button--icon button--icon-right plp-next-btn js-search-loadmore-btn']")))

    index = 24
    while len(loadingButton) > 0:
        driver.execute_script("arguments[0].click();", loadingButton[0])

        i = i + 1
        product_webelements = driver.find_elements("xpath", '//*[@class="product product-grid__product js-grid-tile-product"]')

        try:
            WebDriverWait(driver, 200).until(ec.url_contains(str(24*i)))
        except TimeoutException:
            break

        try:
            loadingButton = WebDriverWait(driver, 200).until(ec.presence_of_all_elements_located((By.XPATH, load_more_btn)))
        except TimeoutException:
            break

    product_webelements = driver.find_elements("xpath", '//*[@class="product product-grid__product js-grid-tile-product"]')


    for product_webelement in product_webelements:
        l = product_webelement.find_elements("xpath", ".//div/div[@class ='product-tile__badge']/div/img")
        if(len(l)>0):
            img_path = l[0].get_attribute('src')
            if "1plus1" in img_path:
                list_url.append(product_webelement.find_element("xpath", ".//div/div/a").get_attribute('href'))


df = pd.DataFrame(list_url)
df.to_csv("etos_1plus1.csv")
