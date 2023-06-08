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
names = []
countrys = []
exhibitor_stands = []
exhibitor_halls = []
websites = []
twitters = []
linkedins = []
instagrams = []
youtubes = []
abouts = []
comp_profiles = []
comp_hqs = []
comp_types = []
short_dess = []


for i in range(1, 65):
    url = "https://gitexafrica.expoplatform.com/newfront/marketplace/exhibitors?limit=12&pageNumber={}".format(i)
    driver.get(url)
    wait_until_component_is_visible(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div/div[2]/div[1]/h2")
    print(i)

    link_list = []

    wait_until_component_is_visible(By.XPATH, "/html/body/div[1]/div[2]/div[1]/main/div/div/div[3]/div/div[2]/div[2]/div[12]/div/div[1]")

    links = driver.find_elements(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-inherit.MuiLink-root.MuiLink-underlineAlways.css-1s3gmda')


    for link in links:
        href_link = link.get_attribute('href')
        if "exhibitor" in href_link:
            link_list.append(href_link)

    link_list = list(set(link_list))
    for link in link_list:
        driver.get(link)

        try:
            name_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-h2.MuiTypography-alignCenter.css-2z6g9m')
            name = name_ele.text
        except NoSuchElementException:
            name = None
        names.append(name)

        try:
            country_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body1.MuiTypography-alignCenter.css-9ryj3r[data-styleid="product-subtitle1')
            country = country_ele.text
        except NoSuchElementException:
            country = None
        countrys.append(country)

        try:
            hall_ele = driver.find_element(By.CSS_SELECTOR, '[data-styleid="exhibitorHall"]')
            hall = hall_ele.text
        except NoSuchElementException:
            hall = None
        exhibitor_halls.append(hall)

        try:
            exhibitor_stand_ele = driver.find_element(By.CSS_SELECTOR, '[data-styleid="exhibitorStand"]')
            exhibitor_stand = exhibitor_stand_ele.text
        except NoSuchElementException:
            exhibitor_stand = None
        exhibitor_stands.append(exhibitor_stand)

        try:
            website_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-subtitle2.MuiTypography-noWrap.css-2v1bp3')
            website = website_ele.text
        except NoSuchElementException:
            website = None
        websites.append(website)

        try:
            twitter_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[3]/div/div/div[2]/div/div[2]/div[2]/a[1]')
            twitter = twitter_ele.get_attribute('href')
        except NoSuchElementException:
            twitter = None
        twitters.append(twitter)

        try:
            instagram_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[3]/div/div/div[2]/div/div[2]/div[2]/a[2]')
            instagram = instagram_ele.get_attribute('href')
        except NoSuchElementException:
            instagram = None
        instagrams.append(instagram)

        try:
            linkedin_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[3]/div/div/div[2]/div/div[2]/div[2]/a[3]')
            linkedin = linkedin_ele.get_attribute('href')
        except NoSuchElementException:
            linkedin = None
        linkedins.append(linkedin)

        try:
            youtube_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[3]/div/div/div[2]/div/div[2]/div[2]/a[4]')
            youtube = youtube_ele.get_attribute('href')
        except NoSuchElementException:
            youtube = None
        youtubes.append(youtube)

        try:
            about_ele = driver.find_element(By.CSS_SELECTOR, '.MuiTypography-root.MuiTypography-body1.css-ztt2f5[data-testid="description"]')
            about = about_ele.text.strip()
        except NoSuchElementException:
            about = None
        abouts.append(about)

        try:
            short_des_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div/div[2]/div/div/p')
            short_des = short_des_ele.text.strip()
        except NoSuchElementException:
            short_des = None
        short_dess.append(short_des)

        try:
            comp_profile_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div/div[3]/div/div/p')
            comp_profile = comp_profile_ele.text.strip()
        except NoSuchElementException:
            comp_profile = None
        comp_profiles.append(comp_profile)

        try:
            comp_hq_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div/div[4]/div/div/p')
            comp_hq = comp_hq_ele.text
        except NoSuchElementException:
            comp_hq = None
        comp_hqs.append(comp_hq)

        try:
            comp_type_ele = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/main/div/div/div/div/div[5]/div/div/div[5]/div/div/p')
            comp_type = comp_type_ele.text
        except NoSuchElementException:
            comp_type = None
        comp_types.append(comp_type)


df = pd.DataFrame({"Company_Name": names, "Country": countrys, "Exhibitor Hall": exhibitor_halls, "Exhibitor_Stand": exhibitor_stands,
                   "Website": websites, "Twitter_id": twitters, "LinkedIn_id": linkedins, "Instagram_id": instagrams,
                   "Youtube_id": youtubes, "About": abouts, "Company_Profile": comp_profiles, "Company_HQ": comp_hqs,
                   "Type_of_Company": comp_types, "Short_Description": short_dess})

df.to_csv('exhibitors_details.csv')

driver.quit()
