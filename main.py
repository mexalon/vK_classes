import requests
import time

VK_ENDPOINT = 'https://api.vk.com/method/'
VK_VER = '5.126'


def get_token(file_name: str):
    """получить токен из файла"""
    with open(file_name, 'r', encoding='utf-8') as f:
        token = f.readline()
    return token


VK_TOKEN = get_token('token.txt')


class User:
    """суперкласс для для учёта всех создаваемых объектов"""
    all_users = {}  # индекс всех объектов классов

    def __init__(self):
        self.all_users.setdefault(type(self).__qualname__, [])
        self.all_users[type(self).__qualname__] += [self]


class VkUser(User):
    """На вход подаётся id или домен пользователя ВК"""
    def __init__(self, some_id):

        some_user = requests.get(VK_ENDPOINT + 'users.get', params={'access_token': VK_TOKEN,
                                                                    'v': VK_VER,
                                                                    'user_ids': some_id,
                                                                    }).json()
        time.sleep(0.5)  # чтобы не забанили, ждём пол секунды
        new_id = None
        new_user = None
        if 'error' in some_user.keys():
            print(some_user['error']['error_msg'])  # криво введён айди, экземпляр остаётся с пустыми атрибутами
        else:
            new_user = some_user
            new_id = some_user['response'][0]['id']
            is_it_old = check_id(new_id)
            if is_it_old:
                print(f'Такой пользовательь уже есть в моём реестре: ID{new_id}')
            else:
                super().__init__()  # прописывается в индекс уникальных объектов

        self.user = new_user
        self.id = new_id

    def __str__(self):
        """Имя Фамилия: ссылка на профиль"""
        output = f"{self.user['response'][0]['first_name']}" \
                 f" {self.user['response'][0]['last_name']}:" \
                 f" https://vk.com/id{self.id}"
        return output

    def __and__(self, other):
        """Поиск общих друзей через соответствующий метод API"""
        mutual_friends = requests.get(VK_ENDPOINT + 'friends.getMutual',
                                      params={
                                          'access_token': VK_TOKEN,
                                          'v': VK_VER,
                                          'source_uid': self.id,
                                          'target_uid': other.id
                                      }).json()
        time.sleep(0.5)
        # каждый объект проходит инициализацию с обращением к users.get поэтому дело не быстрое
        if 'error' in mutual_friends.keys():
            print(mutual_friends['error']['error_msg'])
        if 'response' in mutual_friends.keys():
            output = [VkUser(str(entry)) for entry in mutual_friends['response']]
        else:
            output = []
        return output


def get_id_from_url(url: str):
    """Разбор ссылки профиля"""
    result = url.strip().split('/id')[-1].split('/')[-1]
    if result:
        output = result
    else:
        output = None  # будет ссылка на свой собственный аккаунт

    return output


def add_user(new_id=None):
    """Создание нового объекта"""
    if new_id is None:
        url = input('введите ссылку на пользователя ВК:\n')
        temp_id = get_id_from_url(url)
    else:
        temp_id = new_id

    output = VkUser(temp_id)  # тут может и какой то другой класс создаваться
    if output.user:
        print(f'Добавлен {output}')

    return output


def check_id(some_id):
    """"Проверка, есть ли пользователь с таким ID среди уже созданных экземпляров всех классов
    Возвращает либо имеющийся экземпляр класса, либо False"""
    spam = User()
    spam.all_users.pop(type(spam).__qualname__)
    output = False
    if spam.all_users.keys():
        for entry in spam.all_users.values():
            for item in entry:
                if item.id == some_id:
                    output = item

    return output


def get_mutual_friends():
    """Функция поиска общих друзей
    Возвращает список экземпляров класса - общих друзей, если они есть"""
    urls = input('введите через запятую ссылки на двух пользователей ВК:\n')
    id_list = [get_id_from_url(entry) for entry in urls.split(',')]
    all_trash_entries = [add_user(entry) for entry in id_list]
    good_objects = [entry for entry in all_trash_entries if entry.user]
    if len(good_objects) >= 2:
        result = good_objects[0] & good_objects[1]  # всё как в задании:)
        if result:
            print('Общие друзья:')
            print_users(*result)
            return result
        else:
            print('Нет общих друзей в общем доступе')
    else:
        print('Некорректный ввод пользователей')


def print_all():
    """Вывод всех имеющихся экземпляров всех классов"""
    spam = User()
    spam.all_users.pop(type(spam).__qualname__)
    if spam.all_users.keys():
        for entry in spam.all_users.values():
            print_users(*entry)
    else:
        print('Нет пользователей для вывода')


def print_users(*args):
    for entry in args:
        print(entry)


def help_():
    print('а   – добавить новый объект пользователя;'
          '\nm   – найти общих друзей двух пользователей;'
          '\nall – вывести список всех объектов пользователей;'
          '\nq   – выход.'
          )


def quit_():
    print('Выход')
    raise SystemExit(0)


def get_action(command_: str):
    all_commands_ = {'q': quit_,
                     'a': add_user,
                     'all': print_all,
                     'm': get_mutual_friends,
                     'help': help_
                     }

    if command_ in all_commands_.keys():
        all_commands_[command_]()
    else:
        print('неверная команда')


def go_vk():
    print('Выберите "q" для выхода или "help" для списка доступных команд')
    while True:
        my_command = input('Введите команду:')
        get_action(my_command)


if __name__ == '__main__':
    go_vk()
