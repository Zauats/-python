
import vk_api
import re
from itertools import groupby
import sqlite3


class Main:
    """Класс создает объект, через который можо обращаться к vk_api. Так же собирает данные о пользователе
    при помощи функции get_user, которая описана ниже"""

    def __init__(self, user):
        if not isinstance(user, User):
            raise TypeError("user должен быть типа User")
        self.user = user

    def add_compatibility_points(self, user, peoples):
        # все возможные параметры для сравнивания:
        all_params = ['about', 'activities', 'books', 'games', 'movies', 'music', 'quotes', 'status', 'tv',
                      'common_count', 'personal']
        # параметры, которые есть в поле personal:
        personal = ['political', 'people_main', 'life_main', 'smoking', 'alcohol', 'religion']

        # цикл, который проходится по всем параметрам пользователя и если он подходит для сравнивания, добавляет список
        # так я узнаю, какие по каким параметра нужно смотреть других пользователей
        params = []
        for param in all_params:
            if param in user.user:
                params.append(param)

        """ 
        В этом цикле в словаре с информацией о ползователе добавляется поле compatibility. Это очки совпадения.
        1 общий друг - балл, 1 слово из описания страницы совпадает - 0.2 балла, совпадает что-то из поля personal - 
        0.5 балла за каждое совпадение. Так же добавляется поле params. В нем содержится за что баллы были зачислены 
        и какие слова совпадают
        """
        for people in peoples:
            people['compatibility'] = 0
            people['params'] = {'word_points': 0, 'person_points': 0, 'words': []}

            """
            В этом цикле я ищу совпадения слов со страницы. беру одно поле, проверяю, что оно есть
            и у пользователя и у человека, которого мы нашли. Затем убираю из строк все, кроме букв, цифр и пробелов.
            Разбиваю строки по пробелу, ищу совпадения. Если есть совпадение , добавляю 0.2 балла к очкам совместимости
            """
            for param in params[:-2]:
                if param in people:
                    people_str = re.sub('[^\w\d\s]', '', people[param]).split(' ')
                    user_str = re.sub('[^\w\d\s]', '', user.user[param]).split(' ')
                    for word in user_str:
                        if (word in people_str) and (word != ''):
                            people['params']['words'].append(word)
                            people['compatibility'] += 0.2
                            people['params']['word_points'] += 0.2

            # Добавляю +1 балл за каждого общего друга
            people['compatibility'] += people['common_count']

            # проверка, что personal есть и у пользователи и у человека, что был найден
            if ('personal' in people) and ('personal' in user.user):
                # практически то же самое, что и в предыдущем цикле, только здесь протсо нужно сравнить числа
                for param in personal:
                    if (param in people['personal']) and (param in user.user['personal']):
                        if people['personal'][param] == user.user['personal'][param]:
                            people['compatibility'] += 0.5
                            people['params']['person_points'] += 0.5

        # сортирую список по очкам совместимости

        peoples.sort(key=lambda peoples: peoples['compatibility'])
        return peoples

    def search_peoples(self, user):
        # возвращает список всех возможных людей, которые мне подходят
        people_list = list()  # множество со всеми людьми. Повторов там не будет
        fields = ['about', 'activities', 'books', 'common_count', 'domain', 'games', 'home_town', 'interest', 'movies',
                  'music', 'personal', 'photo_max_orig', 'quotes', 'sex', 'status', 'tv']
        for i, group in enumerate(user.user['groups']):
            # запрашиваем список людей, которые подходят по начальным параметрам и находятся в определенной группе
            try:
                # поиск по группам
                people_list.extend(user.vk.users.search(count=1000, fields=fields,
                                                        city=user.user['city']['id'], sex=user.user['search_sex'],
                                                        country=user.user['country']['id'],
                                                        status=6, age_from=round(user.user['age'] * 0.9),
                                                        age_to=round(user.user['age'] * 1.1),
                                                        has_photo=1, group_id=group['id'])['items']) 
            except:
                print('Что-то пошло не так((')
            print(i)
        try:
            # поиск по глобальному поиску
            people_list.extend(user.vk.users.search(count=1000, fields=fields,
                                                    city=user.user['city']['id'], country=user.user['country']['id'],
                                                    sex=user.user['search_sex'],
                                                    status=6, age_from=round(user.user['age'] * 0.9),
                                                    age_to=round(user.user['age'] * 1.1), has_photo=1,)['items']) 
            
        except:
            print("что-то пошло не так((")
        peoples = [el for el, _ in groupby(people_list)]  # убирем повторы.
        return peoples  # возвращаем список

    def get_top3_photo(self, people, user):
        photos = user.vk.photos.getAll(ownet_id=people['id'], count=200, extended=1)['items']
        top_photos = []
        photos.sort(key=lambda photos: photos['likes']['count'])

        for photo in photos[-3:]:
            top_photos.append({'photo': photo['sizes'][-1]['url'],
                               'likes': photo['likes']['count']})
        return top_photos


class User:

    def __init__(self, login, password, id):
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth(token_only=True)
        self.vk = vk_session.get_api()
        self.id = id
        self.user = self.vk.users.get(user_ids=id,
                                      fields=['about', 'activities', 'bdate', 'books', 'common_count', 'country', 'city',
                                              'domain''games', 'home_town', 'interest', 'movies', 'music', 'personal',
                                              'photo_max_orig', 'quotes', 'sex', 'status', 'tv'])[0]
        self.user['age'] = self.get_age(self.user)
        self.user['groups'] = self.get_groups(self.user)
        self.user['search_sex'] = self.get_seatch_sex(self.user)
        self.user['city'] = self.get_city(self.user)

    def get_city(self, user):
        if 'city' not in user:
            return {'id': input('введите id своего города')}
        else:
            return user['city']

    def get_age(self, user):
        if not isinstance(user, dict):
            raise ValueError("user должен быть класса dict")

        if 'bdate' in user:
            date = user['bdate'].split('.')
            if len(date) == 3:
                age = 2019 - int(date[2])
            else:
                age = int(input('Дата частично скрыта или неккоректна. введите свой возраст'))
        else:
            age = int(input('Дата отсутствует. введите свой возраст'))
        return age

    def get_groups(self, user):
        if not isinstance(user, dict):
            raise ValueError("user должен быть класса dict")

        groups = self.vk.groups.get(user_id=self.id, extended=1, fields=['id', 'screen_name', 'members_count'])['items']
        return groups

    def get_seatch_sex(self, user):
        if user['sex'] == 1:
            search_sex = 2
        elif user['sex'] == 2:
            search_sex = 1
        else:
            search_sex = int(input('Человека какого пола вы ищете? \n'
                                   '2 - мужчина, 1 - женщина, 0 - не имеет значения\n'))

        return search_sex


if __name__ == '__main__':
    conn = sqlite3.connect("VkDataBase.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE vk_peoples
                          (page text, photo1 text, photo2 text,
                           photo3 text)
                       """)
        conn.commit()
    except:
        print('первый запуск уже был')

    login = input("Ввеите логин: ")
    password = input("Введите пароль: ")
    my_id = int(input("Введите свой id: "))
    user = User(login, password, my_id)
    print(user.user)
    main = Main(user)
    peoples = main.search_peoples(user)
    print(len(peoples))
    peoples = main.add_compatibility_points(user, peoples)
    print(len(peoples))
    peoples.reverse()
    start_people = 0
    end_people = 10
    while True:
        top_peoples = []
        for people in peoples[start_people:end_people]:
            photos = main.get_top3_photo(people, user)
            top_peoples.append(
                (f"https://vk.com/id{people['id']}", photos[0]["photo"], photos[1]["photo"], photos[2]["photo"]))

        cursor.executemany("INSERT INTO vk_peoples VALUES (?,?,?,?)", top_peoples)
        conn.commit()
        start_people += 10
        end_people += 10
        print('данные переданы в базу данных')
        if input('Хотите найти еще людей? Для продолжения нажмите Enter, для завершения введите "end": ') == 'end':
            break
