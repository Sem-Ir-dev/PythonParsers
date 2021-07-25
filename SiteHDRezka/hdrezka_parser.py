# Site: rezka.ag
import requests # pip install requests
from bs4 import BeautifulSoup as BS # pip install beautifulsoup4
from datetime import datetime

r_all = requests.get('https://rezka.ag/new/')
r_films = requests.get('https://rezka.ag/new/?filter=last&genre=1')
r_serials = requests.get('https://rezka.ag/new/?filter=last&genre=2')
r_cartoons = requests.get('https://rezka.ag/new/?filter=last&genre=3')
r_anime = requests.get('https://rezka.ag/new/?filter=last&genre=82')

names_list = []

def pars(r):
    soup = BS(r.content, 'html.parser')
    names = (soup.findAll('div', class_ = 'b-content__inline_item-link'))

    for i in names:
        text = i.get_text(' | ', strip = True)
        names_list.append(text)

    date = datetime.now()

    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write('Дата парсинга: {0}\n\n'.format(date))
        for i in names_list:
            f.write(str(i + '\n'))

    print('Сохранено в result.txt')

print('[>Парсер сайта rezka.ag<]\n\
    [ Это программа парсит следующие новинки: \n\
        1) Все новинки\n\
        2) Фильмы\n\
        3) Сериалы\n\
        4) Мультфильмы\n\
        5) Аниме\n\
        6) Отмена ]')

options = input('Введите вариант: ')

if options == '1':
    pars(r_all)

elif options == '2':
    pars(r_films) 

elif options == '3':
    pars(r_serials) 

elif options == '4':
    pars(r_cartoons) 

elif options == '5':
    pars(r_anime) 

elif options == '6':
    pass

else:
    print('Можно ввести только от 1 до 6.')
