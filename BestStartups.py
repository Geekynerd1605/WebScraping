from typing import List, Any
from bs4 import BeautifulSoup
import pandas as pd
import requests

img_links = []
n_data = []
links = []
LI_id = []
CB_id = []
data = []
Cmp_CB = []
Cmp_LI = []
Cmp_WB = []

url = "https://beststartup.ca/meet-british-columbias-12-top-ceos-in-the-industrial-space/"
page_html = requests.get(url)
soup = BeautifulSoup(page_html.text, 'html.parser')

id = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33]
for i in id:
    cl = "wp-container-{0} wp-block-columns alignwide".format(i)

# Scraping the text from each class
    for i in soup.find_all("div", attrs={"class": cl}):
        data.append(i.get_text().strip("\n").split("\n"))

# Getting the links
        for j in i.find_all("ul", attrs={'class': "has-black-color has-white-background-color has-text-color has-background"}):
            for a in j.find_all('a', href=True):
                links.append(a['href'])

# Image URL
        im = i.find_all('img')
        for a in i.find_all('img'):
            if a['src'] is not "":
                img_links.append(a['data-src'])
                # print(a['data-src'])
            else:
                img_links.append('Picture not present')
                # print("Picture not present")

# Storing the name, designation and about in n_data
for id in range(len(data)):
    n_data.insert(id, data[id][0:3])
for ele in n_data:
    df = pd.DataFrame(n_data, columns=['Name', 'Designation', 'About'])

for i in range(len(links)):
    k = links[i]
    if i % 5 == 0:
        CB_id.append(k)
    elif i % 5 == 1:
        LI_id.append(k)
    elif i % 5 == 2:
        Cmp_CB.append(k)
    elif i % 5 == 3:
        Cmp_LI.append(k)
    else:
        Cmp_WB.append(k)

df['LinkedIn']=LI_id
df['Company Website']=Cmp_WB
df['Comp_LI']=Cmp_LI
df['Comp_CB']:Cmp_CB
df['CrunchBase']= CB_id
print(df.head())

df.to_csv('/home/hb/Desktop/Swastika/Web Scraping/Best Startups.csv', sep='\t', encoding='utf-8', index=False)
