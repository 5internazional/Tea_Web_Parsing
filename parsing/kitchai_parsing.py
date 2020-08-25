import requests
from bs4 import BeautifulSoup
import csv

CSV = 'kitchai.csv'
HOST = 'https://kitchai.ru/'
URL = 'https://kitchai.ru/catalog/section/kitayskiy_chay_katalog/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='sellers-item')
    cards = []
    for item in items:
        cards.append(
            {
                'title': item.find('a', class_="sellers-item__name").get_text(strip=True),
                'link_product': HOST + item.find('div', class_='sellers-item__img2').find('a').get('href'),
                'price': item.find('span', class_='price-big').get_text(strip=True),
                'image': HOST + item.find('div', class_='sellers-item__img2').find('a').find('img').get('src')
            })
    return cards

def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Product name', 'Product link', 'Price', 'Image'])
        for item in items:
            writer.writerow([item['title'], item['link_product'], item['price'], item['image']])

def parser():
    PAGENATION = int(input('Enter a number of pages for parsing:').strip())
    html = get_html(URL)
    if html.status_code==200:
        cards = []
        for page in range(1, PAGENATION):
            html = get_html(URL, params={'page': page})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        print(cards)
    else:
        print('error')

parser()