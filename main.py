import requests
import time
from pprint import pprint

VK_ENDPOINT = 'https://api.vk.com/method/'
VK_VER = '5.126'


def get_token(file_name: str):
    """получить токен из файла"""
    with open(file_name, 'r', encoding='utf-8') as f:
        token = f.readline()
    return token


VK_TOKEN = get_token('token.txt')


class VkUser():
    """На вход подаётся id или домен пользователя ВК"""

    def __init__(self, some_id):

        some_user = requests.get(VK_ENDPOINT + 'users.get', params={'access_token': VK_TOKEN,
                                                                    'v': VK_VER,
                                                                    'user_ids': some_id,
                                                                    }).json()
        time.sleep(0.5)  # чтобы не забанили, ждём пол секунды
        new_id = None
        new_user = None
        if not self.chek_error(some_user):
            new_user = some_user
            new_id = some_user['response'][0]['id']

        self.user = new_user
        self.id = new_id

    def __str__(self):
        """Имя Фамилия: ссылка на профиль"""
        if self.user:
            output = f"{self.user['response'][0]['first_name']}" \
                     f" {self.user['response'][0]['last_name']}:" \
                     f" https://vk.com/id{self.id}"
        else:
            output = f'пользователь не определён'

        return output

    def chek_error(self, response_json):
        if 'error' in response_json.keys():
            print(response_json['error']['error_msg'])
            error = response_json['error']['error_code']
        else:
            error = False

        return error

    def get_albums(self):
        if self.id:
            albums = requests.get(VK_ENDPOINT + 'photos.getAlbums',
                                  params={
                                      'access_token': VK_TOKEN,
                                      'v': VK_VER,
                                      'owner_id': self.id,
                                      'need_system': 1
                                  }).json()

            time.sleep(0.5)  # чтобы не забанили, ждём пол секунды
            if not self.chek_error(albums):
                if albums['response']:
                    albums_id_index = list()
                    print(f'{self}\nАльбомы:')
                    for num, item in enumerate(albums['response']['items']):
                        print(f'{num}. {item["title"]}')
                        albums_id_index.append(item['id'])

                    output = albums_id_index
            else:
                output = False
        else:
            output = False

        return output

    def get_photos(self, album_id):
        if self.id:
            photos = requests.get(VK_ENDPOINT + 'photos.get',
                                  params={
                                      'access_token': VK_TOKEN,
                                      'v': VK_VER,
                                      'owner_id': self.id,
                                      'album_id': album_id,
                                      'extended': 1
                                  }).json()

            time.sleep(0.5)  # чтобы не забанили, ждём пол секунды
            if not self.chek_error(photos):
                if photos['response']:
                    photos_id_index = list()
                    print(f'{self}\nФотографии в альбоме {album_id}:')
                    for num, item in enumerate(photos['response']['items']):
                        top_size = self.best_size(item["sizes"])
                        print(f'{num}. {item["id"]} >>Лучший размер {top_size["type"]} >> Лайков: {item["likes"]["count"]} >> добавлена {item["date"]}>> {top_size["url"]}')
                        photos_id_index.append(item['id'])

                    output = photos_id_index
            else:
                output = False
        else:
            output = False

        return output

    def best_size(self, sizes_list):
        type_ = ['s', 'm', 'x', 'o', 'p', 'q', 'r', 'y', 'z', 'w']
        size_ = range(1, len(type_) + 1)
        sizes_rating = dict(zip(type_, size_))
        top_size = sorted(sizes_list, key=(lambda item: sizes_rating[item['type']]), reverse=True)[0]
        return top_size


def get_user_albums(url=None):
    """запрос альбомов пользователя по ссылке"""
    the_user = add_user(url)
    if the_user:
        albums = the_user.get_albums()
        go_albums(the_user, albums)


def go_albums(user, index):
    choice = ''
    print('Выберите номер альбома для скачивания или "n" для выбора другого пользователя:')
    while choice != 'n':
        choice = input().lower().strip()
        if choice.isdigit():
            num = int(choice)
            if 0 <= num < len(index):
                user.get_photos(index[num])
            else:
                print('нет такого альбома')
        else:
            print('не верная команда')


# def y_or_n():
#     done = False
#     while not done:
#         answer = input('(y / n):').lower().strip()
#         if answer == 'y' or answer == 'n':
#             output = answer == 'y'
#             done = True
#     return output


def get_id_from_url(url: str):
    """Разбор ссылки профиля"""
    result = url.strip().split('/id')[-1].split('/')[-1]
    if result:
        output = result
    else:
        output = None  # будет ссылка на свой собственный аккаунт

    return output


def add_user(url=None):
    """Создание нового объекта"""
    if url is None:
        url = input('введите ссылку на пользователя:\n')
        temp_id = get_id_from_url(url)
    else:
        temp_id = get_id_from_url(url)

    new_user = VkUser(temp_id)  # тут может и какой то другой класс создаваться
    if new_user.id:
        output = new_user
    else:
        output = False

    return output


def help_():
    print('ставьте ID пользователя либо ссылку на его профиль и нажмите Enter.\n '
          'После этого Вам будет предложено выбрать альбом для загрузки из списка '
          'альбомов этого пользователя'
          )


def quit_():
    print('Выход')
    raise SystemExit(0)


def get_action(command_: str):
    all_commands_ = {'q': quit_,
                     'help': help_
                     }

    if command_ in all_commands_.keys():
        all_commands_[command_]()
    else:
        get_user_albums(command_)


def go_go():
    print('Вставьте ссылку на пользователя или выберите "q" для выхода, "help" для справки')
    while True:
        my_command = input('Ссылка на профиль: ').lower().strip()
        get_action(my_command)


if __name__ == '__main__':
    go_go()
