import requests
from bs4 import BeautifulSoup
import csv
import random
import psycopg2
from datetime import datetime

#https://www.avito.ru/perm/kvartiry/prodam/3-komnatnye/novostroyka-ASgBAQICAUSSA8YQAkDmBxSOUsoIFIRZ?cd=1&f=ASgBAQECAUSSA8YQAkDmBxSOUsoIFIRZBUXgBxd7ImZyb20iOjUxMzAsInRvIjpudWxsfeIHF3siZnJvbSI6NTE5MiwidG8iOm51bGx9hAkUeyJmcm9tIjo2MCwidG8iOjEwMH2MLhV7ImZyb20iOjExLCJ0byI6bnVsbH2QLhV7ImZyb20iOjExLCJ0byI6bnVsbH0
URL = 'https://www.avito.ru/perm/kvartiry/prodam/3-komnatnye/novostroyka-ASgBAQICAUSSA8YQAkDmBxSOUsoIFIRZ'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
HOST = 'https://www.avito.ru'
FILE = 'ThreeRoom.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code == 200:
        return r.text
    else:
        print('Error get_html')


def get_page():
    with open('G:\Python\parsAvito\page2.html',encoding='utf-8') as f:
        r = f.read()
        return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='snippet-horizontal')
    ads = []
    for item in items:
        title_block = item.find('a', class_='snippet-link')
        title = title_block.get_text(strip=True)
        href = HOST+title_block.get('href')
        price = item.find('span', class_='snippet-price').get_text(strip=True).replace(' ₽', '').replace(' ', '')
        price = int(price)
        adress = item.find('span', class_='item-address__string').get_text(strip=True)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        list = [title,href,price,adress,now]
        ads.append(list)

        #
        # ads.append({
        #     'title': title,
        #     'href': href,
        #     'price': price,
        #     'adress': adress,
        # })

    return ads


def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='pagination-item-1WyVp')

    if pagination:
        return int(pagination[-2].get_text())
    else:
        return 1


def save_file(items, path):
    with open(path,'w',newline='',encoding='utf-8') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(items[0])
        for item in items:
            writer.writerow([item['title'],item['href'],item['price'],item['adress']])
            # writer.writerow([item['title'],item['href'],item['price'],item['adress']])


def save_sql(items):
    conn = psycopg2.connect('postgres://postgres:2126829740@localhost:5432/parserdata')
    cursor=conn.cursor()
    for item in items:
        query = item[0],item[1],item[2],item[3],item[4]
        query = str(query)
        cursor.execute("INSERT INTO appartments(title,href,price,adress,time) VALUES "+query,)

    conn.commit()
    conn.close()


def parse():
    text = get_html(URL)
    # text = get_page()
    ads = get_content(text)
    pages = get_pages(text)
    # p = random.randint(2,5)
    for p in range(2,pages+1):
        text = get_html(URL,params={'p':p})
        ads.extend(get_content(text,))
        print(f'Парсим страницу {p} из {pages}.')
    text = get_html(URL,params={'p':p})
    ads.extend(get_content(text,))

    # save_file(ads, FILE)
    save_sql(ads)




parse()