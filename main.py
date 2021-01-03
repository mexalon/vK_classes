import requests
import time
from pprint import pprint


VK_ENDPOINT = 'https://api.vk.com/method/'
VK_VER = '5.89'


class VkUser:
    def __init__(self, user_id):
        self.id = user_id

    def get_self(self):
        user = requests.get(VK_ENDPOINT + 'users.get', params={'access_token': get_token(),
                                                               'v': VK_VER,
                                                               'user_ids': self.id,
                                                               'fields': 'photo_50'})
        pprint(user.json())


def get_token():
    with open('token.txt', 'r', encoding='utf-8') as f:
        token = f.readline()
    return token




# class OverflowSearch:
#     def __init__(self):
#         pass
#
#     def make_search(self, tag: str, hours=1):
#         """Поиск по тегу за последние hours часов. За день набегает многовато вопросов, решил в часах квантовать"""
#         endpoint = 'https://api.stackexchange.com/2.2/search'
#         now = int(time.time())
#         from_date = str(now - 60 * 60 * hours)
#         numpage = 1
#         the_tag = self.check_tag(tag)
#         if the_tag is None:
#             print(f'There is no {tag} in tags')
#             return [{'title': None}]
#
#         parameters = {'site': 'stackoverflow',
#                       'tagged': tag,
#                       'fromdate': from_date,
#                       'sort': 'creation',
#                       'pagesize': '100',
#                       'page': str(numpage)
#                       }
#         has_it_more = True
#         list_of_things = ['Spam!']
#         print('Collecting pages:')
#         while has_it_more:
#             response = requests.get(endpoint, params=parameters)
#             response.raise_for_status()
#             print(numpage)
#             time.sleep(1)  # чтобы не забанили
#             list_of_things += response.json()['items']
#             has_it_more = response.json()['has_more']
#             numpage += 1
#             parameters['page'] = str(numpage)
#
#         list_of_things.pop(0)
#         output = tuple(list_of_things)
#         return output
#
#     def check_tag(self, tag: str):
#         endpoint = f'https://api.stackexchange.com/2.2/tags/{tag}/info'
#         parameters = {'site': 'stackoverflow'}
#         response = requests.get(endpoint, params=parameters)
#         if response.json()['items']:
#             its_name = response.json()['items'][0]['name']
#         else:
#             its_name = None
#
#         return its_name


def go_vk():
    me = VkUser('1258178')
    me.get_self()


if __name__ == '__main__':
    go_vk()
