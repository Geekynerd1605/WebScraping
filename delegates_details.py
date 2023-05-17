import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


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
driver.find_element('name', "username").send_keys("username")  # Enter username
driver.find_element('name', "password").send_keys("password")  # Enter Password
driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/form/div[4]/button').click()

names = []
designations = []
organisations = []
countrys = []
categorys = []
company_types = []
company_industrys = []
company_industry_sub_techs = []

for i in range(1, 183):
    url = "https://gitexafrica.expoplatform.com/newfront/participants?page=delegates&limit=12&pageNumber={}".format(i)
    driver.get(url)
    wait_until_component_is_visible(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div[1]/div/div/div/button/h5")
    print(i)

    link_list = []

    wait_until_component_is_visible(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div[2]/div/div[1]/div[12]")

    links = driver.find_elements(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineAlways.css-1s3gmda')
    print(len(links))
    for link in links:
        href_link = link.get_attribute('href')
        # print(href_link)
        if "participant" in href_link and "24121" not in href_link:
            link_list.append(href_link)
    # print(link_list)
    print(len(link_list))

    for link in link_list:
        driver.get(link)
        try:
            name_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-h2.MuiTypography-alignCenter.css-2z6g9m')
            name = name_ele.text
            print(name)
        except NoSuchElementException:
            name = None
        names.append(name)

        try:
            designation_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body1.MuiTypography-alignCenter.css-9ryj3r[data-styleid="product-subtitle1"]')
            desig = designation_ele.text
            print(desig)
        except NoSuchElementException:
            desig = None
        designations.append(desig)

        try:
            org_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body1.MuiTypography-alignCenter.css-9ryj3r[data-styleid="product-subtitle2"]')
            org = org_ele.text
            print(org)
        except NoSuchElementException:
            org = None
        organisations.append(org)

        try:
            country_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[2]/div[3]/div/div/div/div/div[1]/div/div/p")
            country = country_ele.text
            print(country)
        except NoSuchElementException:
            country = None
        countrys.append(country)

        try:
            category_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[2]/div[3]/div/div/div/div/div[2]/div/div/p")
            category = category_ele.text
            print(category)
        except NoSuchElementException:
            category = None
        categorys.append(category)

    print(names)
    print(designations)
    print(organisations)
    print(countrys)
    print(categorys)

        # try:
        #     company_type_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[2]/div[3]/div/div/div/div/div[3]/div/div/p")
        #     company_type = company_type_ele.text
        #     print(company_type)
        # except NoSuchElementException:
        #     company_type = None
        # company_types.append(company_type)
        #
        # try:
        #     company_industry_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[2]/div[3]/div/div/div/div/div[4]/div/div/p")
        #     company_industry = company_industry_ele.text
        #     print(company_industry)
        # except NoSuchElementException:
        #     company_industry = None
        # company_industrys.append(company_industry)
        #
        # try:
        #     company_industry_st_ele = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[2]/div[3]/div/div/div/div/div[5]/div/div/p")
        #     company_industry_sub_tech = company_industry_st_ele.text
        #     print(company_industry_sub_tech)
        # except NoSuchElementException:
        #     company_industry_sub_tech = None
        # company_industry_sub_techs.append(company_industry_sub_tech)

df = pd.DataFrame({"Delegate_Name": names, "Designation": designations, "Organisation": organisations,
                   "Country":countrys, "Category": categorys})
                    #, "Company Type": company_types,
                  # "Company Industry": company_industrys, "Company Industry Sub-Technology": company_industry_sub_tech})
df.to_csv('delegates_details.csv')

driver.quit()
