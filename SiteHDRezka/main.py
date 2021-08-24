import requests  # pip install requests
from bs4 import BeautifulSoup as BS  # pip install beautifulsoup4
from datetime import datetime
from tkinter import *
import webbrowser


class Window:
    def __init__(self, width, height, x, y, title, resizeble=(False, False), icon=None):
        self.button_color = '#E0ECE4'
        self.button_color2 = '#F7F2E7'
        self.frame_color = '#D8D3CD'
        self.bg_color = '#FCF8EC'

        self.r_all = requests.get('https://rezka.ag/new/')
        self.r_films = requests.get('https://rezka.ag/new/?filter=last&genre=1')
        self.r_serials = requests.get('https://rezka.ag/new/?filter=last&genre=2')
        self.r_cartoons = requests.get('https://rezka.ag/new/?filter=last&genre=3')
        self.r_anime = requests.get('https://rezka.ag/new/?filter=last&genre=82')

        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.resizable(resizeble[0], resizeble[1])
        self.root['bg'] = self.bg_color
        self.root.iconbitmap(icon)

    def draw_widget(self):
        def pars(r):
            soup = BS(r.content, 'html.parser')
            names = (soup.findAll('div', class_='b-content__inline_item-link'))
            self.names_list = []

            for i in names:
                text = i.get_text(' | \n', strip=True)
                self.names_list.append(text)

        def save_result(data):
            date = datetime.now()

            with open('result.txt', 'a', encoding='utf-8') as f:
                f.write('Дата парсинга: {0}\n\n'.format(date))
                for i in data:
                    f.write(str(i + '\n'))

        def git_open():
            webbrowser.open('https://github.com/Sem-Ir-dev')

        def but_pressed(category):
            pars(category)
            text_widget.delete('1.0', END)
            text_widget.insert(1.0, self.names_list)

        def but_save():
            data = self.names_list
            save_result(data)

        def about():
            about_win = Toplevel(self.root)
            about_win.title('О программе')
            about_win.geometry('300x200+450+200')
            about_win.resizable(False, False)
            Label(about_win, text='Программа, которая \nпарсирует новинки с сайта\n rezka.ag', font='Arial, 16').pack()

        def bt_quit():
            self.root.quit()

        main_menu = Menu(self.root)
        self.root.config(menu=main_menu)

        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label='Сохранить', command=but_save)
        file_menu.add_command(label='Выход', command=bt_quit)

        help_menu = Menu(main_menu, tearoff=0)
        help_menu.add_command(label='GitHub', command=git_open)
        help_menu.add_command(label='О программе', command=about)

        main_menu.add_cascade(label="Файл",
                              menu=file_menu)
        main_menu.add_cascade(label="Справка",
                              menu=help_menu)

        text_widget = Text(self.root, width=44, height=17, bg=self.frame_color, wrap=WORD)
        text_widget.place(x=30, y=30)

        scrollbar = Scrollbar(self.root, bg=self.frame_color)
        scrollbar.place(x=385, y=30, height=275)
        scrollbar['command'] = text_widget.yview
        text_widget['yscrollcommand'] = scrollbar.set

        Label(self.root, text='Парсер сайта rezka.ag', font='Arial, 15', bg=self.bg_color).place(x=190, y=0)
        Label(self.root, text='Made by Sem_Ir', font='Calibri, 9', bg=self.bg_color).place(x=500, y=370)

        Frame(self.root, width=145, height=330, bg=self.frame_color).place(x=436, y=35)

        Button(self.root, text='Все новинки', height='3', width=16, bg=self.button_color,
               activebackground=self.button_color2, command=but_pressed(self.r_all)).place(x=450, y=50)
        Button(self.root, text='Фильмы', height='3', width=16, bg=self.button_color,
               activebackground=self.button_color2, command=but_pressed(self.r_films)).place(x=450, y=110)
        Button(self.root, text='Сериалы', height='3', width=16, bg=self.button_color,
               activebackground=self.button_color2, command=but_pressed(self.r_serials)).place(x=450, y=170)
        Button(self.root, text='Мультфильмы', height='3', width=16, bg=self.button_color,
               activebackground=self.button_color2, command=but_pressed(self.r_cartoons)).place(x=450, y=230)
        Button(self.root, text='Аниме', height='3', width=16, bg=self.button_color,
               activebackground=self.button_color2, command=but_pressed(self.r_anime)).place(x=450, y=290)
        Button(self.root, text='Сохранить в .txt', height='3', width=18, bg=self.button_color,
               activebackground=self.button_color2, command=but_save).place(x=30, y=325)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    window = Window(600, 400, 390, 180, 'HDRezka Parser')
    window.draw_widget()
    window.run()
