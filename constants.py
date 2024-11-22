NORM = '\033[0m'
RED = '\033[91m'
GREEN = '\033[32m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
LIGHTBLUE = '\033[94m'
LIGHTCYAN = '\033[96m'
LIGHTGREEN = '\033[92m'
LIGHTYELLOW = '\033[93m'


choice_dic = {
    0: 'Завершить работу,',
    1: 'Регистрация пользователя,',
    2: 'Вход в систему,',
    3: 'Выход из системы,',
    4: 'Добавить книгу,',
    5: 'Удалить книгу по ID,',
    6: 'Найти и удалить книгу,',
    7: 'Поиск книг по ключевому слову,',
    8: 'Поиск книг по ключевому слову с учетом их наличия,',
    9: 'Взять книгу домой,',
    10: 'Вывести список всех книг,',
    'Любой другой ввод': 'Вывести содержимое всей базы.'
}

status_list = ['в наличии', 'выдана', 'утеряна']
