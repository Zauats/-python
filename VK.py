import vk_api
from pprint import pprint
import json
import time

class Main():
    """Это класс, который принимает логин и пароль от вк, заходит в него и делает определенные действия
        __init__ - создается переменная с данными пользователя и класс vk, через который можно обращаться к api
        get_user - принимает id пользователя и возвращает расширеную информацию
        get_peoples - Это генератор. Берет сама информацию о списке групп из self.user, который был создан при инициализации,
                      с помощью for проходится по всем группам пользователя и возвращает с помощью yield 
                      список пользователей в этой группе. 
        search_top10_people - вызывает генератор get_peoples, берет из него список пользователей, берет топ 10 из них(если так это можно
                              назвать) и возвращает список 10 пользователей с ссылкой на 3 фотографии и аккаунт. Может быть вызвана 
                              несколько раз для получения других результатов. 
        json_parser - принимает то, что нужно перевести в json. создает файл, помещает туда json.
        
        Теперь то, что у меня сделано:
            Программа ищет по возрасту, группам, полу, расположению. Топ пользователей выбирается просто первые десять. Фотографии 
            выбираются по популярности и только три штуки, здесь все нормально. Так же все 10 пользователей записываются в json файл.
            Вместо токена использовал библиотеку, которая позволяет пройт нормальную, человеческую авторизацию.
        
        Баги и прочие недоработки:
        1. По интересам все распределить я не смог, т.к. Вк просто не дает о них информации. Два часа пылътался найти нужный метод.
           Если поймете,что делать, подскажите, как можно подбирать людей по интересам. Я думал убирать из каждых критериев(музыка,
           фильмы, книги и т.д.) все символы, кроме букв и пробелов, весь текст разбить на слова по пробелу и поместить в список, потом
           сравнивать.
        2. Есть баг с вызовом метода users.search(). В нем есть параметр group_id. И ВК документация гласит, что при указании 
           этого параметра поиск ведется в группе указанного id. У меня же при указани id группы, поиск ведется в подписчиках какого-то
           человека с этом id, а не группе. 
           Тесты буду писать в конце
        """

    def __init__(self, login, password):
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth(token_only=True)
        self.vk = vk_session.get_api()
        self.user = self.vk.account.getProfileInfo()
        self.user =self.get_user(self.user['screen_name'])
        self.user['groups'] = self.vk.groups.get()['items']
        self.peoples = self.get_peoples()

    def get_user(self, user_ids):
        user_fields = ['photo_id', 'verified', 'sex', 'bdate', 'city', 'country', 'home_town',
                       'photo_400_orig', 'online', 'domain', 'has_mobile',
                       'contacts', 'site', 'education', 'universities', 'schools', 'status', 'last_seen',
                       'followers_count', 'common_count', 'occupation', 'nickname', 'relatives', 'relation',
                       'personal', 'connections', 'exports', 'activities', 'interests', 'music', 'movies',
                       'tv', 'books', 'games', 'about', 'quotes', 'can_post', 'can_see_all_posts', 'can_see_audio',
                       'can_write_private_message', 'can_send_friend_request', 'is_favorite', 'is_hidden_from_feed',
                       'timezone', 'screen_name', 'maiden_name', 'is_friend', 'friend_status', 'career',
                       'military', 'blacklisted', 'blacklisted_by_me']
        user = self.vk.users.get(user_ids=user_ids, fields=user_fields)[0]
        return user

    
    def get_peoples(self):
        fields = ['photo_id', 'verified', 'sex', 'bdate', 'city', 'country', 'home_town', 'photo_400_orig',
                  'lists', 'domain', 'has_mobile', 'contacts', 'site', 'education', 'universities', 'schools',
                  'status', 'last_seen', 'followers_count', 'common_count', 'occupation', 'nickname', 'relatives',
                  'relation', 'personal', 'connections', 'exports', 'wall_comments', 'activities', 'interests', 'music',
                  'movies', 'tv', 'books', 'games', 'about', 'quotes', 'can_post', 'can_see_all_posts', 'can_see_audio',
                  'can_write_private_message', 'can_send_friend_request', 'is_favorite', 'is_hidden_from_feed', 'timezone',
                  'screen_name', 'maiden_name', 'is_friend', 'friend_status', 'career', 'military', 'blacklisted', 'blacklisted_by_me ']

        if self.user['sex'] == 2:
            sex = 1
        else:
            sex = 2

        for group in self.user['groups']:
            user_age = 2019 - int(self.user['bdate'].split('.')[2])
            peoples = self.vk.users.search(count=1000, fields=fields, city=self.user['city']['id'], country=self.user['country']['id'],
                                           sex=sex, status=6, age_from=user_age * 0.8, age_to=user_age * 1.2, online=1, has_photo=1,
                                           group_id=group)
            yield peoples['items']

    def search_top10_people(self):
        peoples = self.peoples.__next__()
        peoples_list = []
        i = 0
        for people in peoples:
            if i % 3 == 0:
                start = time.time()
            try:
                photos = self.vk.photos.getAll(owner_id=people['id'], extended=1, count=200)['items']
                i += 1
            except:
                continue
            photos.sort(key=lambda photos: photos['likes']['count'])

            peoples_list.append({
                'account': 'https://vk.com/id' + str(people['id']),
                'photo1': photos[-3]['sizes'][4]['url'],
                'photo2': photos[-2]['sizes'][4]['url'],
                'photo3': photos[-1]['sizes'][4]['url']
            })
            if i == 10:
                break
            if i % 3 == 0 and time.time() - start < 1:
                time.sleep(1 - (time.time() - start))
        return peoples_list

    def json_parser(self, user_list):
        with open('file_json.json', 'w', encoding='UTF-8') as f:
            json.dump(user_list, f)

if __name__ == '__main__':
    login = input("Ввеите логин")
    password = input("Введите пароль: ")
    user = Main(login, password)
    user.json_parser(user.search_top10_people())
