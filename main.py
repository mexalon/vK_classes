import requests
import time
from pprint import pprint


VK_ENDPOINT = 'https://api.vk.com/method/'
VK_VER = '5.126'


def get_token(file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        token = f.readline()
    return token


VK_TOKEN = get_token('token.txt')


class User:
    all_users = {}  # индекс всех объектов классов, чтобы было

    def __init__(self):
        self.all_users.setdefault(type(self).__qualname__, [])
        self.all_users[type(self).__qualname__] += [self]


class VkUser(User):
    def __init__(self, some_user):
        """инициализаця объекта через обращение к users.get"""
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

    def get_self(self):
        pprint(self.user)


def print_users(*args):
    for entry in args:
        print(entry)


def get_id_from_url(url: str):
    """Разбор ссылки профиля"""
    result = url.strip().split('/id')[-1].split('/')[-1]
    if result:
        output = result
    else:
        output = None

    return output


def quit_():
    print('Выход')
    return False


def add_user(new_id=None):
    """Создание нового объекта класса пользовалетя ВК.
    Если ID есть в ВК, возвращает новый экземпляр класса
    Если такой экземпляр уже есть, то возвращается ссылка на него.
    Если такого пользователя в ВК нет возвращает True"""
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
    if 'error' in new_user.keys():
        print(new_user['error']['error_msg'])
        output = True
    else:
        proper_id = new_user['response'][0]['id']
        is_it_old = check_id(proper_id)
        if is_it_old:
            print(f'Такой пользовательь уже есть в моём реестре: {proper_id}')
            output = is_it_old
        else:
            output = VkUser(new_user)
    return output


def check_id(some_id):
    """"Проверка, есть ли пользователь с таким ID среди уже созданных экземпляров класса
    Возвращает либо имеющийся экземпляр класса, либо False"""
    spam = User()
    spam.all_users.pop(type(spam).__qualname__)
    if VkUser.__qualname__ in spam.all_users.keys():
        all_id = [entry.id for entry in spam.all_users[VkUser.__qualname__]]
        if some_id in all_id:
            output = spam.all_users[VkUser.__qualname__][all_id.index(some_id)]
        else:
            output = False

    else:
        output = False

    return output


def print_all():
    """Вывод всех имеющихся экземпляров класса"""
    spam = User()
    spam.all_users.pop(type(spam).__qualname__)
    if VkUser.__qualname__ in spam.all_users.keys():
        print_users(*spam.all_users[VkUser.__qualname__])
    else:
        print('Нет пользователей для вывода')
    return True


def get_mutual_friends():
    """Функция поиска общих друзей
    Возвращает список экземпляров - общих друзей, либо True, если друзей нет"""
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
        else:
            print('У этих пользователей нет общих друзей')
            output = True
    else:
        print('Некорректный ввод пользователей')
        output = True

    return output


def get_action(command_: str):
    all_commands_ = {'q': quit_,
                     'a': add_user,
                     'all': print_all,
                     'm': get_mutual_friends
                     }

    if command_ in all_commands_.keys():
        output = all_commands_[command_]()
    else:
        print('неверная команда')
        output = True

    return output


def go_vk():
    go_go = True
    while go_go:
        my_command = input('Введите команду:')
        go_go = get_action(my_command)


if __name__ == '__main__':
    go_vk()
