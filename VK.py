import vk_api
from pprint import pprint
import json
import time
import re


class Main():
    """Класс создает объект, через который можо обращаться к vk_api. Так же собирает данные о пользователе
    при помощи функции get_user, которая описана ниже"""

    def __init__(self, login, password, id):
        # создается переменная с данными пользователя и объект vk, через который можно обращаться к api
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth(token_only=True)
        self.vk = vk_session.get_api()
        self.user = self.get_user(id)

    def run(self):
        """Функция, запускающая приложение. Здесь цикл в каждой итерации проходится по списку людей, взятые из функции search_people(),
           отбирает нужные параметры для записи и записывает их в json файл. Затем предлагает либо поискать еще людей, либо завершить программу
           Не ищу людей сразу во всех группах, т.к их сбор займет очень много времени. Так по-моему удобней."""
        for peoples in self.search_people():
            data = []
            for param in peoples[-10:]:
                data.append({
                    'photo': param['photo_max_orig'],
                    'page': 'https://vk.com/' + param['domain'],
                    'points_compatibility': param['compatibility'],
                    'compatibility': param['params'],
                    'common_friends': param['common_count']
                })
            with open('total_file.json', 'w', encoding="UTF-8") as f:
                json.dump(data, f)

            print('Файл создан')
            if input('Хотите найти еще людей? Для продолжения нажмите Enter, для завершения введите "end": ') == 'end':
                break


    def get_user(self, my_id):
        """Функция принимает id пользователя и возвращает о нем информацию. И если ее не хватает, то запрашивает ее.
        """
        # запрашиваем всю возможную информацию о пользователе
        user = self.vk.users.get(user_ids=my_id, fields=['about', 'activities', 'bdate', 'books', 'common_count', 'country', 'city',
                                                              'domain''games', 'home_town', 'interest', 'movies', 'music', 'personal',
                                                              'photo_max_orig', 'quotes', 'sex', 'status', 'tv'])[0]
        # на случай, если возраст узнать не удалось
        if 'bdate' in user:
            date = user['bdate'].split('.')
            if len(date) == 3:
                user['age'] = 2019 - int(date[2])
            else:
                user['age'] = int(input('введите свой возраст'))
        else:
            user['age'] = int(input('введите свой возраст'))

        # узнаем список групп пользователя
        user['groups'] = self.vk.groups.get(user_id=my_id, extended=1, fields=['id', 'screen_name',
                                                                                    'members_count'])['items']
        # дополнительный вопросы к пользователю:
        user['search_sex'] = int(input('Человека какого пола вы ищете? \n'
                                       '2 - мужчина, 1 - женщина, 0 - не имеет значения\n'))
        user['age_from'] = int(input('От какого возраста вы хотите искать? '))
        user['age_to'] = int(input('До какого возраста вы хотите искать? '))
        return user


    def search_people(self):
        # все возможный параметры для сравнивания:
        all_params = ['about', 'activities', 'books', 'games', 'movies', 'music', 'quotes', 'status', 'tv', 'common_count', 'personal', ]
        # параметры, которые есть в поле personal:
        personal = ['political', 'people_main', 'life_main', 'smoking', 'alcohol', 'religion']

        # цикл, который проходится по всем параметрам пользователя и если он подходит для сравнивания, добавляет список
        # так я узнаю, какие по каким параметра нужно смотреть других пользователей
        params = []
        for param in all_params:
            if param in self.user:
                params.append(param)

        # главный цикл функции в каждой итерации он находит список людей, которые мне подоходят и находятся в определенной группе
        for group in self.user['groups']:
            # запрашиваем список людей, которые подходят по начальным параметрам и находятся в определенной группе groups
            peoples = self.vk.users.search(count=1000, fields=['about', 'activities', 'books', 'common_count',
                                                                  'domain', 'games', 'home_town', 'interest', 'movies', 'music', 'personal',
                                                                  'photo_max_orig', 'quotes', 'sex', 'status', 'tv'],
                                           city=self.user['city']['id'], country=self.user['country']['id'], sex=self.user['search_sex'],
                                           status=6, age_from=self.user['age_from'], age_to=self.user['age_to'],
                                           has_photo=1, group_id=group['id'])['items']

            """в этом цикле в словаре с информацией о ползователе добавляется поле compatibility. Это очки совпадения
               1 общий друг - балл, 1 слово из описания страницы совпадает - 0.2 балла, 
               совпадает что-то из поля personal - 0.5 балла за каждое совпадение.
               Так же добавляется поле params. В нем содержится за что баллы были зачислены и какие слова совпадают
            """
            for people in peoples:
                people['compatibility'] = 0
                people['params'] = {'word_points': 0, 'person_points': 0, 'words': []}

                """В этом цикле я ищу совпадения слов со страницы. беру одно поле, проверяю, что оно есть
                   и у пользователя и у человека, которого мы нашли. Затем убираю из строк все, кроме букв, цифр и пробелов.
                   Разбиваю строки по пробелу, ищу совпадения. Если совпадение обнаруживается, добавляю 0.2 балла к очкам совместимости
                """
                for param in params[:-2]:
                    if param in people:
                        people_str = re.sub('[^\w\d\s]', '', people[param]).split(' ')
                        user_str = re.sub('[^\w\d\s]', '', self.user[param]).split(' ')
                        for word in user_str:
                            if (word in people_str) and (word != ''):
                                people['params']['words'].append(word)
                                people['compatibility'] += 0.2
                                people['params']['word_points'] += 0.2

                # Добавляю +1 балл за каждого общего друга
                people['compatibility'] += people['common_count']

                # проверка, что полу personal есть и у пользователи и у человека, что был найден
                if ('personal' in people) and ('personal' in self.user):
                    # практически то же самое, что и в предыдущем цикле, только здесь протсо нужно сравнить числа
                    for param in personal:
                        if (param in people['personal']) and (param in self.user['personal']):
                            if people['personal'][param] == self.user['personal'][param]:
                                people['compatibility'] += 0.5
                                people['params']['person_points'] += 0.5

            # сортирую список по очкам совместимости
            peoples.sort(key=lambda peoples: peoples['compatibility'])
            yield peoples



if __name__ == '__main__':
    login = input("Ввеите логин")
    password = input("Введите пароль: ")
    id = int(input("Введите свой id"))
    user = Main('+79653417551', 'zxcvbnm12.', 187509567)
    user.run()
