import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

driver.maximize_window()
driver.get("https://www.kruidvat.nl/")

driver.implicitly_wait(20)
time.sleep(15)
driver.find_element("id", "onetrust-accept-btn-handler").click()

driver.execute_script("window.scrollTo(0, 0);")

time.sleep(4)

a = ActionChains(driver)
m = driver.find_element("xpath", "//v-slot[@name='link']//a[@title='Beauty'][normalize-space()='Beauty']")
a.move_to_element(m).perform()

time.sleep(1)

items_list = driver.find_elements("xpath", "//*[@class='nav__link-inner--sub']")
category_url_list = []
for items in items_list:
    category_url_list.append(items.get_attribute('href'))

list_set = set(category_url_list)
category_url_list = (list(list_set))

product_link_with_roundel = []

for url in category_url_list:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    number_of_pages = 0
    for i in soup.find_all("div", attrs={"class": "pager__range"}):
        name = i.get_text()
        name = name.strip("\n").strip(" ").split("\n")
        res = []
        for ele in name:
            if ele.strip():
                res.append(ele)

        if len(res) > 3:
            number_of_pages = int(res[-2].strip(" "))
    base_url = url

    for page in range(number_of_pages):
        url = base_url + "?page=" + str(page) + "&size=20&sort=ratingLSP"

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        for i in soup.find_all("div", attrs={"class": "product__list-col"}):
            name = i.get_text()
            link_product = ""
            for a in i.find_all('a', href=True):
                link_product = a['href']

            images = i.findAll('img')
            for image in images:
                temp = '\t'.join(image['class'])
                if 'roundel' in temp:
                    if "1003.png" in image['data-src']:
                        product_link_with_roundel.append(link_product)

df = pd.DataFrame(product_link_with_roundel)

df.to_csv("kruidvat.csv")
