import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


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
    return url



def get_content(url):
    content = []
    for urls in url:
        soup = get_soup(urls)
        tittle = soup.find('h1', class_='title').text
        vac_info = soup.find('div', class_= 'vacancy__info__body').text
        vac_text = soup.find('div', class_='vacancy__text').text
        vac_agent = soup.find('a', class_='button button--blue button--mobile-fluid js-vacancy-apply--manually gtm-track-jobs-vacancy-button')['href']
        content.append((tittle, vac_info, vac_text, vac_agent))

        print(vac_info)

def main():
    get_soup(URL)
    url = get_url()
    get_content(url)



if __name__ == '__main__':
    main()