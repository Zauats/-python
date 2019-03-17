import vk_api
from pprint import pprint
import json
import time

class Main():
    """Это класс, который принимает логин и пароль от вк, заходит в него и делает определенные действия
        __init__ - создается переменная с данными пользователя и класс vk, через который можно обращаться к api
        get_user - принимает id пользователя и возвращает расширеную информацию
        get peoples - берет сама информацию из пг"""

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
    user = Main('+79653417551', 'zxcvbnm12.')
    user.json_parser(user.search_top10_people())
