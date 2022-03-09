from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("C:\Users\rajee\Desktop\game\project127\chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers = ["Proper name", "Distance", "Mass", "Radius"]
star_data = []
new_star_data=[]
def scrape():
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for tr_tag in soup.find_all("th", attrs={"class", "headerSort"}):
            th_tags = tr_tag.find_all("th")
            temp_list = []
            for index, tr_tag in enumerate(th_tags):
                if index == 0:
                    temp_list.append(th_tags.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(th_tags.contents[0])
                    except:
                        temp_list.append("")
            star_data.append(temp_list)

def scrape_more_data(url):
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_brown_dwarfs'
        page=requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        star_table=soup.find_all('table')
        table_rows=star_table[7].find_all('tr')
        for table_rows in soup.find_all("tr", attrs={"class", "headerSort"}):
            td_tags = table_rows.find_all("td")
            temp_list = []
            for td_tag in td_tags:
                    try:
                        temp_list.append(td_tag.find_all(("div"),attrs={'class':'value'})[0].contents[0])
                    except:
                        temp_list.append("")
            new_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(url)

scrape()

for index,data in enumerate(star_data):
    scrape_more_data(data[7])
    print(f'{index+1}page done 2')

final_star_data=[]

for index,data in enumerate(star_data):
    new_star_data_element=new_star_data[index]
    new_star_data_element=[elem.replace('\n','')for elem in new_star_data_element]
    final_star_data.append(data+new_star_data_element)

with open("scrapper_stars.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_star_data)
