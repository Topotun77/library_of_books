import json
import logging
from dataclasses import asdict, dataclass

from constants import *
from utilities import color


def loging_decor(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info(result)
        return result

    return wrapper


@dataclass
class User:
    """
    Класс пользователя. Содержит логин, хеш пароля, возраст
    """
    user: str
    passwd: str
    age: int

    def __init__(self, user, passwd, age):
        self.user = user
        self.passwd = passwd
        self.age = age
        # age - некоторые книги могут быть 18+ (зарезервировано для дальнейшего использования
        # т.к. поля с возрастными ограничениями для класса Book не было в техническом задании,
        # но в дальнейшем может появиться, а пользователи у нас уже будут с возрастом)

    def __str__(self):
        return self.user


@dataclass
class Book:
    """
    Класс: Книга.
    Аттрибуты:
    id (уникальный идентификатор, генерируется автоматически)
    title (название книги)
    author (автор книги)
    year (год издания)
    status (статус книги: “в наличии”, “выдана”)
    """
    # id: int
    title: str
    author: str
    year: int
    status: str
    max_id = 0

    def __init__(self, title: str, author: str, year: int, status: str = 'в наличии'):
        """
        Инициализация объекта класса Book
        Пояснение: уникальность id организована через глобальную переменную max_id
        """
        Book.max_id += 1
        self.id = Book.max_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        """
        Вывод информации о книге
        :return: строка для печати
        """
        return self.title

    def __repr__(self):
        """
        Технический вывод информации о книге
        :return: строка для печати
        """
        list_ = list(map(lambda x, y: '\n\t' + str(x) + ' = ' + str(y), self.__dict__.keys(),
                         self.__dict__.values()))
        return f' '.join(list_)


@dataclass
class LibraryOfBooks:
    """
    Класс: Библиотека книг.
    Содержит путь к файлу с данными, список пользователей, список книг, текущего пользователя
    и различные методы работы с ними
    """
    users: list[User]
    books: list[Book]

    def __init__(self, bd_patch='bd.json'):
        self.bd_patch = bd_patch
        self.users: list[User] = []
        self.books: list[Book] = []
        self.current_user: User | None = None
        self.__read_json()

    def __str__(self):
        """
        Вывод информации об объекте.
        1. Список пользователей
        2. Список книг
        :return: Строка с текущим пользователем, т.к. весь вывод осуществляется внутри метода
        """
        print(color('\nСписок пользователей:\n', CYAN))
        for i in self.users:
            print('\t' + str(i))

        print(color('\nСписок книг:', CYAN))
        for i in self.books:
            print(repr(i))

        return f'\n{color('Текущий пользователь', CYAN)} {self.current_user}\n'

    # def __setattr__(self, key, value):
    #     if key in ['users', 'books']:
    #         self.__write_json()

    def __read_json(self):
        """
        Приватный метод, позволяющий считывать данные из файла .json
        :return: None
        """
        if not self.bd_patch:
            return
        try:
            with open(self.bd_patch, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.books = [Book(**item) for item in data[0]]
            self.users = [User(**item) for item in data[1]]
        except Exception as er:
            logging.error(f'Ошибка чтения файла: {er.args}')

    def __write_json(self):
        """
        Приватный метод, позволяющий сохранять данные в файл .json
        :return: None
        """
        try:
            if not self.bd_patch:
                return
        except AttributeError:
            pass
        try:
            data_json = [[asdict(book) for book in self.books],
                         [asdict(user) for user in self.users]]
        except Exception as er:
            logging.error(f'Ошибка формирования данных для выгрузки в файл: {er.args}', stack_info=True)
            return
        try:
            with open(self.bd_patch, 'w', encoding='utf-8') as f:
                json.dump(data_json, f, indent=4, ensure_ascii=False)
        except Exception as er:
            logging.error(f'Ошибка записи файла: {er.args}', stack_info=True)

    def contains_user(self, user_name: str, passwd=None) -> int | None:
        """
        Метод проверяет, существует ли пользователь в базе.
        :param user_name: Имя пользователя для проверки наличия.
        :param passwd: Хеш пароля (сам пароль не сохраняется ни в одной переменной на протяжении
               работы всей программы).
        :return: Номер позиции, либо None, в случае, если ничего не найдено.
        """
        for i in range(len(self.users)):
            if str(self.users[i]) == str(user_name):
                if passwd is None:
                    return i
                if self.users[i].passwd == passwd:
                    return i
        return None

    def contains_book(self, book_name: str, available=True) -> int | None:
        """
        Метод проверяет, существует ли книга в базе.
        :param book_name: Название книги для проверки наличия.
        :param available: Учитывать наличие книги при поиске.
        :return: Номер позиции, либо None, в случае, если ничего не найдено.
        """
        for i in range(len(self.books)):
            if (str(self.books[i]).lower() == str(book_name).lower()
                    and (not available or self.books[i].status == 'в наличии')):
                return i
        return None

    @loging_decor
    def register(self, user, passwd: str, passwd_confirm: str, age: int) -> str:
        """
        Регистрация пользователя в системе.
        :param user: Имя пользователя.
        :param passwd: Пароль.
        :param passwd_confirm: Повторный ввод пароля.
        :param age: Возраст.
        :return: Успех/неудача.
        """
        if self.contains_user(user) is None:
            if passwd == passwd_confirm:
                self.users += [User(user, passwd, age)]
                txt = color(f'Пользователь {user} успешно зарегистрирован.', CYAN)
                txt += '\n' + self.log_in(str(user), passwd)
            else:
                return color('Пароль и повторный ввод пароля не совпадают. Пользователь не создан.', RED)
        else:
            return color(f'Пользователь {user} уже существует.', RED)
        self.__write_json()
        return txt

    def log_in(self, user_name: str, passwd):
        """
        Вход пользователя в систему.
        :param user_name: Имя пользователя.
        :param passwd: Хеш пароля.
        """
        usr = self.contains_user(user_name=user_name, passwd=passwd)
        if usr is not None:
            self.current_user = self.users[usr]
            txt = f'Пользователь {user_name} вошел в систему.'
            logging.info(txt)
            return color(txt, LIGHTBLUE)
        else:
            txt = 'Неверные имя пользователя и пароль. Вход не был выполнен.'
            logging.info(f'Неудачная попытка входа в систему {user_name} {passwd} ' + txt)
            return color(txt, RED)

    @loging_decor
    def log_out(self):
        """
        Выход из системы
        :return: None
        """
        txt = f'Пользователь {self.current_user} покинул нас.'
        self.current_user = None
        return color(txt, LIGHTCYAN)

    def add_book(self, *books: Book) -> str:
        """
        Метод добавляет книгу
        :param books: список объектов класса Book
        :return: результат выполнения по каждому элементу списка
        """
        lst_result = []
        for bk in books:
            # if self.contains_book(book_name=bk.title, available=False) is not None:
            #     txt = f'Книга "{bk.title}" не была добавлена, так как она уже есть в базе.'
            #     logging.info(txt)
            #     lst_result.append(color(txt, RED))
            # else:
            self.books.append(bk)
            txt = f'Книга "{bk.title}" успешно добавлена.'
            logging.info(txt)
            lst_result.append(color(txt, CYAN))
        self.__write_json()
        return '\n'.join(lst_result)

    @loging_decor
    def del_book(self, book: Book) -> str:
        """
        Метод удаляет книгу по ее ID.
        :param book: Объект класса Book
        :return: Успех/неудача
        """
        if self.current_user is None:
            return color(f'Войдите в свой аккаунт чтобы удалить книгу "{book}".')
        if self.contains_book(book_name=book.title, available=False) is None:
            return color(f'Книга "{book.title}" не была найдена в базе.', RED)
        else:
            self.books.remove(book)
            self.__write_json()
            return color(f'Книга "{book.title}" удалена успешно.', CYAN)

    def find_books(self, find_str: str | int, available=False) -> list[Book] | Book:
        """
        Метод get_book принимает поисковое слово и возвращает список названий
        всех книг, содержащих поисковое слово. Поиск осуществляется без учета регистра.
        :param find_str: Слово для поиска.
        :param available: Учитывать наличие книги при поиске.
        :return: Список всех найденных книг.
        """
        res = []
        for i in self.books:
            if isinstance(find_str, int):
                if i.id == find_str:
                    return i
            else:
                if (str(find_str).lower() in str(i.title).lower()
                        and (not available or i.status == 'в наличии')):
                    res.append(i)
                if (str(find_str).lower() in str(i.author).lower()
                        and i not in res
                        and (not available or i.status == 'в наличии')):
                    res.append(i)
                try:
                    if int(find_str) == i.year:
                        res.append(i)
                except ValueError:
                    pass
        return res

    def show_all_books(self):
        """
        Отображение всех книг: Приложение выводит список всех книг с их id, title, author, year и status.
        :return: None
        """
        print(color('\nСписок всех книг:', LIGHTCYAN))
        for i in self.books:
            print(i.title, color(repr(i), CYAN), '\n')

    @loging_decor
    def change_status_book(self, book: Book, status='выдана') -> str:
        """
        Изменение статуса книги: Пользователь вводит id книги и новый статус (“в наличии” или “выдана”).
        :param book: Объект класса Book
        :param status: Статус, на который хотим поменять
        :return: успех/неудача
        """
        if self.current_user is None:
            return color(f'Войдите в свой аккаунт чтобы взять книгу "{book}".')
        book.status = status
        self.__write_json()
        return color(f'Изменения внесены успешно.', CYAN)


if __name__ == '__main__':
    pass
