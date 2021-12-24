import requests
from bs4 import BeautifulSoup
import re
import sqlite3


FILE = 'file.json'
URL = "https://cars.av.by/filter?brands[0][brand]=634&page="

HEADERS = {
    'user-agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "accept": "*/*"
    }
PAGE_COUNT = 3

def get_soup(url, **kwargs):
    r = requests.get(url, **kwargs)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features='html.parser')
    else:
        soup = None
    return soup

def crawl_produkts(page_count):
    pagination = get_soup(URL).find('h3', class_='listing__title').text
    if len(pagination)==24:
        c = pagination [8:9]
        b = pagination[10:13]
        a= c + b
    elif len(pagination)==23:
        page=pagination[8:12]
    elif len(pagination)== 22:
        page = pagination[8:11]
    elif len(pagination)== 21:
        page = pagination[8:10]
    page = (int(page)//25) +1
    urls=[]
    fmt = URL+'{page}'
    print(fmt)
    for i in range(1,PAGE_COUNT):
        print('page:{}'.format(i))
        page_url = fmt.format(page=i)
        print(page_url)
        soup =get_soup(page_url).find_all("div", class_='listing-item')

        if soup is None:
            break
        for tag in soup:
            domen = "https://cars.av.by"
            a = domen +tag.find('a',class_='listing-item__link').get('href')
            urls.append(a)
    return urls

def parse_product(urls):
    cars = []
    for urli in urls:
        print(urli)
        soup = get_soup(urli)
        title = re.sub(r'\xa0',' ',soup.find('h1', class_='card__title').text)
        content = "Описание отсутствует"
        content_full = re.sub(r'\xa0',' ',soup.find("div", class_='card__comment-text'))
        if content_full:
            content = re.sub(r'\xa0',' ',soup.find("div", class_='card__comment-text').text)
        prise = re.sub(r"\u200b|\u2009|\u200a|\xa0", " ", soup.find('div', class_= 'card__price-primary').text)
        img = soup.find('img', class_='lazyload').get("data-src")
        cars.append((title, prise, content, img))
    return cars


def main():
    urls = crawl_produkts(PAGE_COUNT)
    cars = parse_product(urls)
    conn = sqlite3.connect("my_data.db")
    cursor = conn.cursor()
    cursor.executemany("INSERT into switch values (?, ?, ?, ?)", cars)
    conn.commit()
    conn.close()

if __name__ =="__main__":
    main()
