import requests
import time
from pprint import pprint


VK_ENDPOINT = 'https://api.vk.com/method/'
VK_VER = '5.126'


class VkUser:
    def __init__(self, some_id):
        self.user = requests.get(VK_ENDPOINT + 'users.get', params={'access_token': get_token(),
                                                                    'v': VK_VER,
                                                                    'user_ids': some_id,
                                                                    'fields': 'counters, '
                                                                              'domain'}).json()
        self.id = self.user['response'][0]['id']
        time.sleep(0.5)



    def __str__(self):
        output = f"https://vk.com/id{self.id}"
        return output

    def __and__(self, other):
        self.mutual_friends = requests.get(VK_ENDPOINT + 'friends.getMutual',
                                           params={
                                                'access_token': get_token(),
                                                'v': VK_VER,
                                                'source_uid': self.id,
                                                'target_uid': other.id
                                                   }).json()
        return self.mutual_friends
        time.sleep(0.5)




    def get_self(self):
        pprint(self.user)


def get_token():
    with open('token.txt', 'r', encoding='utf-8') as f:
        token = f.readline()
    return token



"""стереть тут не забыть!"""
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

    it1 = VkUser('belindr')

    it2 = VkUser('adres.zanyat')

    pprint(it1 & it2)



if __name__ == '__main__':
    go_vk()
