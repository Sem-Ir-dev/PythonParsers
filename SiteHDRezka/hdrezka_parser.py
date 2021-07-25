# Site: rezka.ag
import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime

r = requests.get('https://rezka.ag/new/')
html = BS(r.content, 'html.parser')
names = (html.findAll('div', class_ = 'b-content__inline_item-link'))

print('Список новинок фильмов на сайте HDRezka')
names_list = []

for i in names:
    print('Фильм:')
    text = i.get_text(' | ', strip = True)
    print(text)
    names_list.append(text)

date = datetime.now()

with open('result.txt', 'a') as f:
    f.write('Дата парсинга: {0}\n'.format(date))
    for i in names_list:
        f.write(str(i + '\n'))
