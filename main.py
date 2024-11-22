from hashlib import sha1
from models import Book, LibraryOfBooks
from constants import *
from utilities import color
import logging


def register_user():
    """Регистрация пользователя"""
    try:
        print(lb.register(input('Введите имя пользователя для регистрации: '),
                          sha1(input('Введите пароль: ').encode()).hexdigest(),
                          sha1(input('Повторите пароль: ').encode()).hexdigest(),
                          int(input('Введите возраст: '))))
    except ValueError as er:
        print(color('Вероятнее всего, Вы неправильно ввели возраст', RED))
        logging.error(er.args)


def login_user():
    """Вход в систему пользователя"""
    print(lb.log_in(input('\nВведите имя пользователя для входа: '),
                    sha1(input('Введите пароль: ').encode()).hexdigest()))


def add_book():
    """Добавить книгу"""
    print(lb.add_book(Book(input('Введите Название книги: '), input('Введите автора книги: '),
                           int(input('Год выпуска книги: ')))))


def del_book():
    """Удалить книгу"""
    try:
        try:
            id = int(input('Введите ID книги, которую хотите удалить :\n'))
        except ValueError:
            txt = color('Неверный тип ID', RED)
            print(txt)
            return
        book = lb.find_books(id)
        if not book:
            print(color('Ничего не найдено!'))
            return
        yes_no = input(f'\nЭту книгу вы хотите удалить:\n{color(repr(book), CYAN)}\nВведите Y/N: ').lower()
        if yes_no == 'y':
            print(lb.del_book(book))
    except Exception as er:
        txt = color('Что-то пошло не так :(', RED)
        logging.error(f'{txt} {er.args}')
        print(txt)


def find_and_del_book():
    """Найти и удалить книгу"""
    str_find = input('Введите название книги, которую хотите удалить :\n')
    try:
        lst_book = lb.find_books(str_find)
        if not lst_book:
            print(color('Ничего не найдено!'))
        for bk in lst_book:
            yes_no = input(f'\nЭту книгу вы хотите удалить:\n{color(repr(bk), CYAN)}\nВведите Y/N: ').lower()
            if yes_no == 'y':
                print(lb.del_book(bk))
                break
    except Exception as er:
        txt = color('Что-то пошло не так :(', RED)
        logging.error(f'{txt} {er.args}')
        print(txt)


def change_status():
    """Изменить статус книги"""
    str_find = input('Введите строку для поиска книги, которую Вы хотите взять домой: \n')
    try:
        lst_book = lb.find_books(str_find, available=True)
        for bk in lst_book:
            yes_no = input(f'\nЭту книгу вы хотите взять:\n{repr(bk)}\nВведите Y/N: ').lower()
            if yes_no == 'y':
                print(lb.change_status_book(bk))
                break
    except:
        print(color('Что-то пошло не так :(', RED))


def find_book(available=False):
    """Поиск книги"""
    lst_result = lb.find_books(input('Введите строку для поиска книг: '), available)
    print(color('Список найденных книг:', LIGHTCYAN))
    for i in lst_result:
        print(i.title, color(repr(i), CYAN), '\n')


if __name__ == '__main__':
    logging.basicConfig(
        filename='library_books.log', filemode='a', encoding='utf-8',
        format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        level=logging.DEBUG)

    lb = LibraryOfBooks()
    choice_action = 1

    while choice_action:
        try:
            txt = '\nВыберете одно из следующих действий:\n' + ''.join(list(map(lambda x, y: '\t' + str(x) +
                  ' = ' + str(y) + '\n', choice_dic.keys(), choice_dic.values())))
            choice_action = input(color(txt, LIGHTYELLOW))
            choice_action = int(choice_action) if choice_action.isnumeric() else 100
            if choice_action == 0:
                exit()
            if choice_action == 1:
                register_user()
            elif choice_action == 2:
                login_user()
            elif choice_action == 3:
                print(lb.log_out())
            elif choice_action == 4:
                add_book()
            elif choice_action == 5:
                del_book()
            elif choice_action == 6:
                find_and_del_book()
            elif choice_action == 7:
                find_book()
            elif choice_action == 8:
                find_book(available=True)
            elif choice_action == 9:
                change_status()
            elif choice_action == 10:
                lb.show_all_books()
            else:
                print(lb)
        except Exception as err:
            logging.error(f'Возникла ошибка {err.args}')
            print(color(f'Возникла ошибка,\nно мы продолжим работу дальше', RED))
