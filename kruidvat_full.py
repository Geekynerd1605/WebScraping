import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
driver.maximize_window()

# driver.get("https://www.kruidvat.nl/a/3578811/max-factor-rimmel-en-bourjois/")  #get method to hit url on  browser
driver.get("https://www.kruidvat.nl/")


driver.implicitly_wait(20)

time.sleep(15)
driver.find_element('id', "onetrust-accept-btn-handler").click()

print(driver.title)
print(driver.current_url)

driver.execute_script("window.scrollTo(0, 0);")  # Scroll to top

time.sleep(15)

a = ActionChains(driver)
# m = driver.find_element_by_xpath("//a[@title='Beauty']//font//font[contains(text(),'Beauty')]")
m = driver.find_element('xpath', "//v-slot[@name='link']//a[@title='Beauty'][normalize-space()='Beauty']")
a.move_to_element(m).perform()  # To hover

time.sleep(15)

items_list = driver.find_elements('xpath', "//*[@class='nav__link-inner--sub']")
category_url_list = []
for items in items_list:
    print(items.get_attribute('href'))
    category_url_list.append(items.get_attribute('href'))

list_set = set(category_url_list)
# convert the set to the list
category_url_list = (list(list_set))

# print(category_url_list)
# print(len(category_url_list))

list_url = []

# category_url_list = ["https://www.kruidvat.nl/beauty/make-up/c/20018"]

for category_url in category_url_list:
    time.sleep(15)
    print(category_url)

    driver.get(category_url)
    product_webelements = []
    clicktimes = 0

    while (1):
        time.sleep(15)
        product_webelements = driver.find_elements('xpath', '//*[@class="tile__product-slide-image-container"]')

        # print(len(product_webelements))

        for product_webelement in product_webelements:
            l = product_webelement.find_elements('xpath', ".//div[@class ='roundel']/img")
            # print(len(l))
            if (len(l) > 0):
                img_path = l[0].get_attribute('data-src')
                # print(img_path)
                if "1003.png" in img_path:
                    # print(img_path)
                    list_url.append(product_webelement.find_element('xpath', ".//a").get_attribute('href'))

        next_pages = driver.find_elements('xpath', "//div[@class='pager plp-paginator__pager pager--mobile-bottom']//e2-link[@title='volgende pagina']")
        # print(len(next_pages))
        if len(next_pages) > 0:
            next_pages[0].click()
            clicktimes = clicktimes + 1
        else:
            break
        if clicktimes > 1:
            break

# print(len(list_url))
print(list_url)

df = pd.DataFrame(list_url, columns=['link'])
print(df)
df.to_csv('kruidvat_final.csv')
