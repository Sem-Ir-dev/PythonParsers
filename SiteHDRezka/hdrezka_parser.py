import requests # pip install requests
from bs4 import BeautifulSoup as BS # pip install beautifulsoup4
from datetime import datetime
from tkinter import *
import webbrowser

def pars(r):
    soup = BS(r.content, 'html.parser')
    names = (soup.findAll('div', class_ = 'b-content__inline_item-link'))

    global names_list
    names_list = []

    for i in names:
        text = i.get_text(' | \n', strip = True)
        names_list.append(text)

def save_result(data):
    date = datetime.now()

    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write('Дата парсинга: {0}\n\n'.format(date))
        for i in data:
            f.write(str(i + '\n'))

def bt_quit():
    window.quit()

def about():
    about_win = Toplevel(window)
    about_win.title('О программе')
    about_win.geometry('300x200+450+200')
    about_win.resizable(False, False)
    Label(about_win, text='Программа, которая \nпарсирует новинки с сайта\n rezka.ag', font='Arial, 16').pack()

def git_open():
    webbrowser.open('https://github.com/Sem-Ir-dev')

def but1_pressed():
    pars(r_all)
    text1.delete('1.0', END)
    text1.insert(1.0, names_list)

def but2_pressed():
    pars(r_films)
    text1.delete('1.0', END)
    text1.insert(1.0, names_list)

def but3_pressed():
    pars(r_serials)
    text1.delete('1.0', END)
    text1.insert(1.0, names_list)

def but4_pressed():
    pars(r_cartoons)
    text1.delete('1.0', END)
    text1.insert(1.0, names_list)

def but5_pressed():
    pars(r_anime)
    text1.delete('1.0', END)
    text1.insert(1.0, names_list)

def but6_pressed():
    data = names_list
    save_result(data)

r_all = requests.get('https://rezka.ag/new/')
r_films = requests.get('https://rezka.ag/new/?filter=last&genre=1')
r_serials = requests.get('https://rezka.ag/new/?filter=last&genre=2')
r_cartoons = requests.get('https://rezka.ag/new/?filter=last&genre=3')
r_anime = requests.get('https://rezka.ag/new/?filter=last&genre=82')

button_color = '#E0ECE4'
button_color2 = '#F7F2E7'
frame_color = '#D8D3CD'
bg_color = '#FCF8EC'

window = Tk()
window.title('HDRezka Parser')
window.geometry('600x400+390+180')
window.resizable(False, False)
window['bg'] = bg_color

main_menu = Menu(window)
window.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Сохранить', command=but6_pressed)
file_menu.add_command(label='Выход', command=bt_quit)

help_menu = Menu(main_menu, tearoff=0)
help_menu.add_command(label='GitHub', command=git_open)
help_menu.add_command(label='О программе', command=about)

main_menu.add_cascade(label="Файл",
                     menu=file_menu)
main_menu.add_cascade(label="Справка",
                     menu=help_menu)

text1 = Text(window, 
    width=50, 
    height=18,
    bg=frame_color,
    wrap=WORD)

text1.place(x=30, y=30)

scrollbar = Scrollbar(window, 
    bg=frame_color)

scrollbar.place(x=385, y=30, height=275)
scrollbar['command'] = text1.yview
text1['yscrollcommand'] = scrollbar.set

Label(window, 
    text='Парсер сайта rezka.ag', 
    font='Arial, 15', 
    bg=bg_color).pack()

Label(window, 
    text='Made by Sem_Ir',
    font='Calibri, 9', 
    bg=bg_color).place(x=500, y=370)

Frame(window, 
    width=145, 
    height=330, 
    bg=frame_color).place(x=430, y=30)

Button(window, 
    text='Все новинки', 
    height='3', 
    width=16, 
    bg=button_color, 
    activebackground=button_color2, 
    command=but1_pressed).place(x=450, y=50)

Button(window, 
    text='Фильмы', 
    height='3', width=16, 
    bg=button_color, 
    activebackground=button_color2,
    command=but2_pressed).place(x=450, y=110)

Button(window, 
    text='Сериалы', 
    height='3', 
    width=16, 
    bg=button_color, 
    activebackground=button_color2, 
    command=but3_pressed).place(x=450, y=170)

Button(window, 
    text='Мультфильмы', 
    height='3', 
    width=16, 
    bg=button_color, 
    activebackground=button_color2,
    command=but4_pressed).place(x=450, y=230)

Button(window, 
    text='Аниме', 
    height='3', 
    width=16, 
    bg=button_color, 
    activebackground=button_color2,
    command=but5_pressed).place(x=450, y=290)

Button(window, 
    text='Сохранить в .txt', 
    height='3', 
    width=18, 
    bg=button_color, 
    activebackground=button_color2,
    command=but6_pressed).place(x=30, y=325)

window.mainloop()
