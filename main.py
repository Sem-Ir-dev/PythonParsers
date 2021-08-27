from tkinter import *
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import webbrowser


class Window:
    def __init__(self, width, height, x, y, title, resizable=(False, False), icon=None):
        self.bg_blue = '#483F98'
        self.bg_active_blue = '#6458D3'
        self.text_bg = '#E5E4F9'
        self.white = '#ffffff'

        self.root = Tk()
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.title(title)
        self.root.resizable(resizable[0], resizable[1])
        self.root.iconbitmap(icon)
        self.root['bg'] = self.white

    def draw_widget(self):
        # ======================= Book Parser ===============
        def create_book_window():
            book_window = Toplevel(self.root)

            book_window.title('Fantasy-Worlds Parser')
            book_window.geometry('600x400+390+180')
            book_window.resizable(False, False)
            book_window['bg'] = self.white

            def page_clear():
                ls.delete('1.0', END)
                e_input.delete(0, END)

            def page_get():
                ls.delete('1.0', END)

                page = e_input.get()
                if page:
                    link = 'https://fantasy-worlds.org/lib/' + page

                    r = requests.get(link)
                    soup = BeautifulSoup(r.content, 'html.parser')

                    name_list = []
                    desc_list = []

                    for name in soup.select('.news_title a'):
                        name_list.append(name.get_text() + '\n')

                    for desc in soup.findAll("span", itemprop="description"):
                        desc_list.append(desc.get_text() + '\n\n')

                    dictionary = dict(zip(name_list, desc_list))

                    for key, value in dictionary.items():
                        ls.insert(END, '-------------------Название----\n')
                        ls.insert(END, key)
                        ls.insert(END, '-------------------Описание----\n')
                        ls.insert(END, value)
                        ls.insert(END, '-------------------------------\n')

            book_title = Label(book_window, text='Парсер сайта Fantasy-World', font='ComicSansMS 16', bg=self.white)
            book_title.place(x=150, y=5)

            page_lb = Label(book_window, text='Выберите страницу:', font='ComicSansMS 12', bg=self.white)
            page_lb.place(x=400, y=40)

            ls = Text(book_window, width=45, height=21, wrap=WORD, bg=self.text_bg, bd=0)
            ls.place(x=20, y=40)

            e_input = Entry(book_window, width=16, font='ComicSansMS 14', bg=self.text_bg)
            e_input.place(x=400, y=70)

            bt_add = Button(book_window, text='Добавить', font='ComicSansMS 14', command=page_get, width=16, height=2,
                        bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                        activeforeground=self.white)
            bt_add.place(x=400, y=110)

            bt_del = Button(book_window, text='Очистить', font='ComicSansMS 14', command=page_clear, width=16, height=2,
                        bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                        activeforeground=self.white)
            bt_del.place(x=400, y=180)

        def create_film_window():
            film_window = Toplevel(self.root)

            film_window.title('HDRezka Parser')
            film_window.geometry('600x400+390+180')
            film_window.resizable(False, False)
            film_window['bg'] = self.white

            self.r_all = requests.get('https://rezka.ag/new/')
            self.r_films = requests.get('https://rezka.ag/new/?filter=last&genre=1')
            self.r_serials = requests.get('https://rezka.ag/new/?filter=last&genre=2')
            self.r_cartoons = requests.get('https://rezka.ag/new/?filter=last&genre=3')
            self.r_anime = requests.get('https://rezka.ag/new/?filter=last&genre=82')

            def pars(r):
                soup = BeautifulSoup(r.content, 'html.parser')
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
                Label(about_win, text='Программа, которая \nпарсирует новинки с сайта\n rezka.ag',
                      font='Arial, 16').pack()

            def bt_quit():
                film_window.quit()

            main_menu = Menu(film_window)
            film_window.config(menu=main_menu)

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

            text_widget = Text(film_window, width=45, height=21, wrap=WORD, bg=self.text_bg, bd=0)
            text_widget.place(x=30, y=30)

            Label(film_window, text='Парсер сайта rezka.ag', font='ComicSansMS 16', bg=self.white).place(x=190, y=0)

            Button(film_window, text='Все новинки', font='ComicSansMS 14', width=16, height=2,
                   bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                   activeforeground=self.white, command=but_pressed(self.r_all)).place(x=410, y=30)
            Button(film_window, text='Фильмы', font='ComicSansMS 14', width=16, height=2,
                   bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                   activeforeground=self.white, command=but_pressed(self.r_films)).place(x=410, y=90)
            Button(film_window, text='Сериалы', font='ComicSansMS 14', width=16, height=2,
                   bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                   activeforeground=self.white, command=but_pressed(self.r_serials)).place(x=410, y=150)
            Button(film_window, text='Мультфильмы', font='ComicSansMS 14', width=16, height=2,
                   bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                   activeforeground=self.white, command=but_pressed(self.r_cartoons)).place(x=410, y=210)
            Button(film_window, text='Аниме', font='ComicSansMS 14', width=16, height=2,
                   bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                   activeforeground=self.white, command=but_pressed(self.r_anime)).place(x=410, y=270)
            Button(film_window, text='Сохранить в .txt', font='ComicSansMS 14', width=16, height=2,
                   bd=0, bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                   activeforeground=self.white, command=but_save).place(x=410, y=330)


        # ======================= Main Menu ===============

        title_lb = Label(self.root, text='Список парсеров:', font='ComicSansMS 24', bg=self.white)
        title_lb.place(x=70, y=20)

        films_bt = Button(self.root, text='Парсер Сериалов', font='ComicSansMS 14', width=19, height=3, bd=0,
                          bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                          activeforeground=self.white, command=create_film_window)
        films_bt.place(x=90, y=80)

        books_bt = Button(self.root, text='Парсер Книг', font='ComicSansMS 14', width=19, height=3, bd=0,
                          bg=self.bg_blue, fg=self.white, activebackground=self.bg_active_blue,
                          activeforeground=self.white, command=create_book_window)
        books_bt.place(x=90, y=180)

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    window = Window(400, 400, 500, 180, 'MyWindow')
    window.draw_widget()
    window.run()
