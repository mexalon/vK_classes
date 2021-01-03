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
    all_users = {}  # индекс всех объектов классов, на всякий случай

    def __init__(self):
        self.all_users.setdefault(type(self).__qualname__, set())
        self.all_users[type(self).__qualname__].add(self)


class VkUser(User):
    def __init__(self, some_id):
        """инициализаця объекта через обращение к users.get"""
        super().__init__()
        self.user = requests.get(VK_ENDPOINT + 'users.get', params={'access_token': VK_TOKEN,
                                                                    'v': VK_VER,
                                                                    'user_ids': some_id,
                                                                    'fields': 'counters, '
                                                                              'domain'}).json()
        self.user.raise_for_status()
        self.id = self.user['response'][0]['id']
        time.sleep(0.5)  # чтобы не забанили, ждём пол секунды

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
        self.mutual_friends.raise_for_status()
        time.sleep(0.5)
        # каждый объект проходит инициализацию с обращением к users.get поэтому дело не быстрое
        output = [VkUser(str(entry)) for entry in self.mutual_friends['response']]
        return output

    def get_self(self):
        pprint(self.user)


def print_users(*args):
    for entry in args:
        print(entry)


def get_id_from_url(url: str):
    return url.split('/')[-1].split('id')[-1]


def quit_():
    print('Quit')
    return False


def add_user():
    url = input('введите ссылку на пользователя ВК:\n')
    temp_id = get_id_from_url(url)

    VkUser(temp_id)
    return True


def print_all():
    spam = User()
    spam.all_users.pop(type(spam).__qualname__)
    if VkUser.__qualname__ in spam.all_users.keys():
        print_users(*spam.all_users[VkUser.__qualname__])
    else:
        print('Нет пользователей для вывода')
    return True


def get_mutual_friends():
    pass


def test():
    pass


def get_action(command_: str):
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
    all_commands_ = {'q': quit_,
                     'a': add_user,
                     'all': print_all,
                     'mut': get_mutual_friends,
                     'test': test}
    go_vk()
