"""
Для наглядности тестирование реализовано моделированием различных ситуаций.
Можно реализовать через Unittest.
"""
import json
from dataclasses import asdict

from models import User, Book, LibraryOfBooks
from constants import *
from utilities import color
from main import *


if __name__ == '__main__':
    b1 = Book('Book1', 'Autor', 2024)
    print(b1)
    print(color(repr(b1), BLUE))
    print(color(repr(b1), LIGHTBLUE))

    lb = LibraryOfBooks()
    b2 = Book('1986', 'Оруэлл', 1999)
    b3 = Book('Python для чайников', 'Гвидо ван Россум', 1986)
    b4 = Book('Python для чайников', 'Гвидо ван Россум', 1986)

    # Добавление книг
    print('\nДобавление книг:')
    print(lb.add_book(b1, b2, b3, b4))
    print(lb)
    lb.show_all_books()

    # Проверка поиска
    print('Результат поиска по "Ору":', lb.find_books('Ору'), sep='\n')
    print('Результат поиска по "1986":', lb.find_books('1986'), sep='\n')

    # Попытка изменить статус книги, не войдя в аккаунт - должна быть ошибка
    print('\nПопытка изменить статус книги, не войдя в аккаунт - должна быть ошибка')
    print(lb.change_status_book(b3))

    # Проверка на вход пользователя
    print('\nПроверка регистрации пользователя')
    print(lb.register('vasya_pupkin', sha1('lolkekcheburek'.encode()).hexdigest(),
                      sha1('lolkekcheburek'.encode()).hexdigest(), 13))
    print(lb.register('pythonist', sha1('iScX4vIJClb9YQavjAgF'.encode()).hexdigest(),
                      sha1('iScX4vIJClb9YQavjAgF'.encode()).hexdigest(), 25))

    print('\nПопытка изменить статус книги, после входа в систему')
    print(lb.change_status_book(b3))

    print('\nПроверка повторной регистрации пользователя')
    print(lb.register('vasya_pupkin',sha1('F8098FM8fjm9jmi'.encode()).hexdigest(),
                      sha1('F8098FM8fjm9jmi'.encode()).hexdigest(), 55))

    # Вывести текущего пользователя
    print('\nТекущий пользователь:', lb.current_user)

    # Попытка входа с неправильным паролем и вход с правильным паролем
    print('\nПопытка входа с неправильным паролем и вход с правильным паролем:')
    print(lb.log_in('vasya_pupkin', sha1('F8098FM8fjm9jmi'.encode()).hexdigest()))
    print(lb.log_in('vasya_pupkin', sha1('lolkekcheburek'.encode()).hexdigest()))

    print('\nПоменять статус:')
    print(lb.change_status_book(b3))

    print('\nПоиск книг по строке "book":')
    print(lb.find_books('book'))

    print('\nВывести всю информацию:')
    print(lb)

    print('\nУдаление всех ранее добавленных книг:')
    print(lb.del_book(b1))
    print(lb.del_book(b2))
    print(lb.del_book(b3))
    print(lb.del_book(b4))

    print('\nВывести всю информацию:')
    print(lb)

    # data_json = [[asdict(book) for book in lb.books],
    #              [asdict(user) for user in lb.users]]
    # with open(lb.bd_patch, 'w', encoding='utf-8') as f:
    #     json.dump(data_json, f, indent=4, ensure_ascii=False)
