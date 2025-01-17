import requests
from bs4 import BeautifulSoup
import json

url = "https://egov.kz/cms/ru/online-services/for_citizen"  # здесь урл

def get_services(url = url):  # здесь парсим сайт
    try:
        soup = BeautifulSoup(requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content, 'html.parser')
        return [{'name': s.text.strip(),
                 'link': s['href'].replace('/cms/ru/online-services/for_citizen', url)}
                for s in soup.find('div', class_='egov-list online-services-list').find_all('a', href=True)]
    except:
        return []


def save_and_search():  # все приколы тут, и сейвит в джсон и поисковик делает, супер!!!
    services = get_services()
    if not services:
        print("не нашлось")
        return

    with open('egov_services.json', 'w', encoding='utf-8') as f:
        json.dump(services, f, ensure_ascii=False, indent=2)

    while True:
        q = input('\nищи что надо (напиши "пока" чтобы выйти отсюда): ').lower().strip()
        if q == 'пока': break

        found = [s for s in services if q in s['name'].lower()]
        if found:
            print(f'\nнашлось {len(found)} штук:')
            for i, s in enumerate(found, 1):
                print(f"{i}. {s['name']} -> {s['link']}")
        else:
            print('ничего нет, давай по новой')


if __name__ == '__main__':
    save_and_search()