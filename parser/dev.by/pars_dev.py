import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv
import re

telegram_token = '2082353800:AAEbBdNfVbXKjOg-2_1v8cfI1RKU6N-d7Dk'
chat_id = '425007240'


file = "vac.csv"
ua = UserAgent()

URL = "https://jobs.dev.by/?filter[specialization_title]=Python"

header = {'User-Agent': str(ua.chrome)}


def get_soup(URL):
    r = requests.get(URL, headers=header)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features='html.parser')
    return soup

def get_url():
    url = []
    f = []
    soup = get_soup(URL).find_all('div', class_='vacancies-list-item__position')
    for item in soup:
        urls = item.find('a', class_='vacancies-list-item__link_block')['href']
        final_url = 'https://jobs.dev.by'+urls
        if final_url == None:
            f.append(final_url)
        else:
            url.append(final_url)
    def get_premium():
        soup1 = get_soup(URL).find_all('div', class_='vacancies-list-item__body premium-vacancy__wrap js-vacancies-list-item--open')
        for item in soup1:
            urls = item.find('a', class_='vacancies-list-item__link_block')['href']
            final_url = 'https://jobs.dev.by'+urls
            if final_url == None:
                f.append(final_url)
            else:
                url.append(final_url)
    get_premium()
    return url


def get_content(url):
    content = []
    for urls in url:
        soup = get_soup(urls)
        vac1 = soup.find('div', class_= 'vacancy__info-block').text
        b = re.sub('Уровень', '\nУровень', vac1)
        c = re.sub('Опыт', '\nОпыт', b)
        d = re.sub('Зарплата', '\nЗарплата', c)
        content.append({
            'title': soup.find('h1', class_='title').text,
            'vac_info': d,
            'vac_text': soup.find('div', class_='vacancy__text').text,
            'vac_agent': soup.find('a', class_='button button--blue button--mobile-fluid js-vacancy-apply--manually gtm-track-jobs-vacancy-button')['href']
        })
    return content

def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Вакансия', 'Требования', 'Полный текст', 'Ссылка'])
        for item in items:
            writer.writerow([item['title'], item['vac_info'], item['vac_text'], item['vac_agent']])

def send_document(filename, telegram_token, chat_id):
    url = 'https://api.telegram.org/bot2082353800:AAEbBdNfVbXKjOg-2_1v8cfI1RKU6N-d7Dk/sendDocument'
    data = {'chat_id': chat_id, 'caption': 'Результат парсинга'}
    with open(filename, 'rb')as f:
        files = {'document': f}
        resp = requests.post(url, data = data, files = files)
        print(resp.json())



def main():
    get_soup(URL)
    url = get_url()
    content = get_content(url)
    print(content)
    save_file(content, file)
    send_document(file, telegram_token, chat_id)



if __name__ == '__main__':
    main()