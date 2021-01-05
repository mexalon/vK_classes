import requests
import time


VK_ENDPOINT = 'https://api.vk.com/method/'
VK_VER = '5.126'


def get_token(file_name: str):
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
    """На вход подаётся json пользователя ВК"""
    def __init__(self, some_user):
        super().__init__()
        self.user = some_user
        self.id = some_user['response'][0]['id']

    def __str__(self):
        """Имя Фамилия: ссылка на профиль"""
        output = f"{self.user['response'][0]['first_name']}" \
                 f" {self.user['response'][0]['last_name']}:" \
                 f" https://vk.com/id{self.id}"
        return output

    def __and__(self, other):
        """Поиск общих друзей через соответствующий метод API"""
        self.mutual_friends = requests.get(VK_ENDPOINT + 'friends.getMutual',
                                           params={
                                                'access_token': VK_TOKEN,
                                                'v': VK_VER,
                                                'source_uid': self.id,
                                                'target_uid': other.id
                                                   }).json()
        time.sleep(0.5)
        # каждый объект проходит инициализацию с обращением к users.get поэтому дело не быстрое
        output = [add_user(str(entry)) for entry in self.mutual_friends['response']]
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
    """Создание нового объекта класса пользовалетя ВК.
    Если такого ID нет в ВК, возвращает False
    Если ID есть в ВК, возвращает новый экземпляр класса
    Если такой экземпляр уже есть, то возвращается ссылка на него."""
    if new_id is None:
        url = input('введите ссылку на пользователя ВК:\n')
        temp_id = get_id_from_url(url)
    else:
        temp_id = new_id

    new_user = requests.get(VK_ENDPOINT + 'users.get', params={'access_token': VK_TOKEN,
                                                                'v': VK_VER,
                                                                'user_ids': temp_id,
                                                               }).json()
    time.sleep(0.5)  # чтобы не забанили, ждём пол секунды
    output = False
    if 'error' in new_user.keys():
        print(new_user['error']['error_msg'])
    else:
        proper_id = new_user['response'][0]['id']
        is_it_old = check_id(proper_id)
        if is_it_old:
            print(f'Такой пользовательь уже есть в моём реестре: {proper_id}')
            output = is_it_old
        else:
            output = VkUser(new_user)  # создание экземпляра объекта
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
    users = [entry for entry in all_trash_entries if isinstance(entry, VkUser)]
    if len(users) >= 2:
        result = users[0] & users[1]  # всё как в задании:)
        if result:
            output = result
            print('Общие друзья:')
            print_users(*output)
            return output
        else:
            print('У этих пользователей нет общих друзей')
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
