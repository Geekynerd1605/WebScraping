import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


# Open the Chrome browser and navigate to the login page
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("https://gitexafrica.expoplatform.com/")
driver.maximize_window()
driver.implicitly_wait(10)


def wait_until_component_is_visible(by, path, counts=None):
    if counts is None:
        counts = []
    isVisible = driver.find_elements(by, path)
    if isVisible:
        return
    else:
        if len(counts) >= 20:
            raise Exception(f"Element on path {path} not found")
        logging.info(f"***  Wait for {path} to get visible count {len(counts)}***")
        time.sleep(120)
        return wait_until_component_is_visible(by, path, counts=counts)

wait_until_component_is_visible(By.XPATH, '//html/body/div[1]/header/div[2]/div[2]/a[2]')

# Login
driver.find_element(By.XPATH, '//html/body/div[1]/header/div[2]/div[2]/a[2]').click()
driver.find_element('name', "username").send_keys("")  # Enter username
driver.find_element('name', "password").send_keys("")  # Enter Password
driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[4]/button').click()

# driver.find_element(By.XPATH, "/html/body/div[1]/header/div[1]/nav/div[3]").click()
products = []
companys = []
countrys = []
exhibitor_halls = []
exhibitor_stands = []
categorys = []
infos = []

for i in range(1, 46):
    url = "https://gitexafrica.expoplatform.com/newfront/marketplace/products?limit=12&pageNumber={}".format(i)
    driver.get(url)
    wait_until_component_is_visible(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div/div[2]/div[1]/h2")
    print(i)

    link_list = []

    wait_until_component_is_visible(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div/div[2]/div[2]/div[12]/div/div[2]/div[1]/a")

    links = driver.find_elements(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineAlways.css-1s3gmda')
    # print(len(links))

    for link in links:
        href_link = link.get_attribute('href')
        # print(href_link)
        if "product" in href_link:
            link_list.append(href_link)
        link_list = list(set(link_list))
    # print(link_list)
    print(len(link_list))

    for link in link_list:
        driver.get(link)
        try:
            name_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-h1.css-trbt65[data-tour="product-title"]')
            name = name_ele.text
            print(name)
        except NoSuchElementException:
            name = None
        products.append(name)

        try:
            company_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-h3.css-16eng5t')
            company = company_ele.text
            print(company)
        except NoSuchElementException:
            company = None
        companys.append(company)

        try:
            country_ele = driver.find_element(By.CSS_SELECTOR, 'MuiTypography-root.MuiTypography-subtitle2.css-pqjh2a')
            country = country_ele.text
            print(country)
        except NoSuchElementException:
            country = None
        countrys.append(country)

        try:
            exhibitor_hall_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div[2]/div/div[2]/div[3]/div/span/span[1]')
            exhibitor_hall = exhibitor_hall_ele.text
            print(exhibitor_hall)
        except NoSuchElementException:
            exhibitor_hall = None
        exhibitor_halls.append(exhibitor_hall)

        try:
            exhibitor_stand_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div/div[2]/div/div[2]/div[3]/div/span/span[3]")
            exhibitor_stand = exhibitor_stand_ele.text
            print(exhibitor_stand)
        except NoSuchElementException:
            exhibitor_stand = None
        exhibitor_stands.append(exhibitor_stand)

        try:
            category_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div/div[3]/div/div/div/div/a/div")
            category = category_ele.text
            print(category)
        except NoSuchElementException:
            category = None
        categorys.append(category)

        try:
            info_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div/div[4]/div/div[2]/div")
            info = info_ele.text
            print(info)
        except NoSuchElementException:
            info = None
        infos.append(info)


df = pd.DataFrame({"Product_Name": products, "Company": companys, "Country": countrys, "Exhibitor_Hall": exhibitor_halls,
                   "Exhibitor_Stand": exhibitor_stands, "Category": categorys, "Product_Info": infos})

df.to_csv('products_details.csv')

driver.quit()



