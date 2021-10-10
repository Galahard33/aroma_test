import re
import requests
from bs4 import BeautifulSoup
import csv

URL = "https://cars.av.by/filter?brands[0][brand]=1850"
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
    'accept': '*/*',
}
HOST = 'https://cars.av.by'
FILE = 'cars.csv'

def get_html(url, params=None):
    r = requests.get(url, headers= HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('h3', class_='listing__title').get_text()
    if len(pagination)==24:
        c = pagination [8:9]
        b = pagination[10:13]
        a= c + b
    elif len(pagination)==23:
        page=pagination[8:12]
    elif len(pagination)== 22:
        page = pagination[8:11]
    elif len(pagination)== 21:
        page= pagination[8:10]
    page = (int(page)//25) +1
    return page
   ## ТУТА


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='listing-item')

    cars=[]

    for item in items:
        cars.append({
            'title': item.find('h3', class_='listing-item__title').get_text(),
            'link': HOST + item.find('a', class_='listing-item__link').get('href'),
            'price': re.sub(r"\u200b|\u2009|\u200a|\xa0", " ", item.find('div', class_='listing-item__price').get_text()),
            'location': item.find('div', class_='listing-item__location').get_text()
        })
    return (cars)


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена', 'Город'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['price'], item['location']])




def parse():
    URL = input('Введите URL: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        page_count = get_pages_count(html.text)
        for page in range(1, page_count + 1):
            print(f'Обработка страницы {page} из {page_count}')
            html = get_html(URL, params={'&page=': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
    else:
        print('Error')


parse()

