import requests
from bs4 import BeautifulSoup


URL = "https://zhodino.gde.by/"

HEADERS = {
    'user-agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "accept": "*/*"
    }


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params= params)
    return r



def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_="content")
    car=[]

    for item in items:
        car.append(
           item.find('a', class_='').get('href'),
        )
    return (car)



def parse():
    html = get_html(URL)
    get_content(html.text)
    print()



parse()

