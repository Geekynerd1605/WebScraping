from bs4 import BeautifulSoup
import argparse
import requests
import csv
import re
import os

data = []
header = []

def parse_arguments():
    parser = argparse.ArgumentParser(description='Pass the url and name and path of the file')
    parser.add_argument('-u', action='store', dest='url', help='Required url link', required=True)
    parser.add_argument('-path', type=dir_path, required=True)
    return parser

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

for page in range(1, 150):
    url = "https://taqeem.gov.sa/en/members-list/?cpage="+str(page)
    page_html = requests.get(url)
    soup = BeautifulSoup(page_html.text, 'html.parser')

    if page == 1:
        header = soup.find("div", attrs={"class":"ast-row ast-row-cols-12 header ast-hidden-xs ast-hidden-sm"}).text.strip("\n").split("\n")
        while '' in header:
            header.remove('')
        header = [x.strip(' ') for x in header]
        print(header)

    for i in soup.find_all("div", attrs={"class": "ast-row ast-row-cols-12"}):
        name = i.get_text()
        name = name.strip("\n").split("\n")
        filter_name = []
        for j in range(len(name)):
            name[j] = re.sub(r'[^a-zA-Z 0-9@.-]', '', name[j])
            name[j] = name[j].strip(' ').strip('\n')
            filter_name.append(name[j])
        while '' in filter_name:
            filter_name.remove('')
        data.append(filter_name)
    print(page)

with open('Table.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(header)
    write.writerows(data)

if __name__ == '__main__':
    args = parse_arguments().parse_args()
    print()
