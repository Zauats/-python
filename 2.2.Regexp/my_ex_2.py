import re
import csv


class PrettyContactsList:
    def __init__(self, contacts):
        self.new_contacts_list = contacts  # главный список со всеми контактами

    def correction_name(self):  # корректирует ФИО
        nice_contacts_list = []  # список, в котором будут новые, исправленные контакты
        for people in self.new_contacts_list[1:]:
            # print([people[0], people[1], people[2]], '-> ', end='')
            people_list = f'{people[0]} {people[1]} {people[2]}'.strip().split(' ')
            # print(people_list)
            """
            объеденяю первые три элемента списка в одну строку. 
            Получается строка с ФИО в Таком виде: 'Имя Фамилия Отчество'
            Затем сразу убираю крайние пробельные символы и разбиваю по пробелу. Получается список такого вида: 
            [Имя, Фамилия, Отчество].Как преминить здесь регулярные выражения, я без понятия. Зачем я соединяю 
            все через пробел, а потом соеденяю через него же? Потому что изначально имена записаны вот так:
            [имя фамилия,' ','отчество'] или так [имя, 'фамилия отчество',]. Это нужно привести к нормальному виду.
            То есть в каждой ячейке списка, имя, фамилия, отчество. По-этому я объеденяю все в такую строку:
            'Имя Фамилия Отчество' и по разделителю привожу в правильный формат. Без пробелов, я бы не смог разделить
            их по ячейкам списка правильно. Возможно и смог бы разделить с помощью регулярных выражений, 
            но это будет гораздо сложнее. Нужно будет составить выражение на Фамилию, Имя, Отчество, придумывать что-то
            с окончаниями. Впрочем я запарюсь. К тому же правило инженера - работает, не трогай. В этой функции я 
            закоментировал код. Это наглядный пример как все преобразуется. К этому добавляем данные, что были и готово
            """
            if len(people_list) == 2:
                people_list.append(
                    '')  # на стучай, если в записях была только имя и фамилия, что бы не ломать структуру контакта.
                # То есть, если было вот так [Фамилия, Имя], добавится третий элемент
            people_list.extend(people[3:])  # добавляю остальные данные, что были в изначальном списоке и воаля, у нас
            # тот же контакт, но с нормально записыными ФИО
            nice_contacts_list.append(people_list)  # добавляю контакт в список со всеми контаками
        self.new_contacts_list = nice_contacts_list  # обновляю контактную книгу

    def correction_number(self):  # Корректирует номер
        nice_contacts_list = []  # список, в котором будут новые, исправленные контакты
        for contact in self.new_contacts_list:

            if len(contact[5]) > 0:  # Условие, проверяющее на то, что у контакта вообще есть телефонный номер
                contact[5] = re.sub('[\D]', '',
                                    contact[5])  # если что, то под пятым индексом переменной contact телефонный номер
                # убираю из телефонного номера все, что мешает, преведению к одному формату.
                # Как вы и посоветовали, оставил одни цифры
                people_number = f'+7({contact[5][1:4]}){contact[5][4:7]}-{contact[5][7:9]}-{contact[5][9:11]}'
                # создаю новый телефонный номер, в правильном формате
                if len(contact[5]) > 11:
                    people_number += f' доб.{contact[5][11:]}'  # добавляю добавочный номер, если он есть

                contact[5] = people_number  # заменяю старый номера на новый стандарт
            nice_contacts_list.append(contact)  # добавляю контакт с измененным номером в книгу
        self.new_contacts_list = nice_contacts_list  # обновляю контактную книгу

    def correction_repetitions(self):  # Убирает повторы
        nice_contact_list = list(self.new_contacts_list)
        # новый список контактов. Из него удалю повторы и добавлю объедененный контакт
        index = 1
        """
        Вкратсе объясню, как все работает. В основном цикле перечисляются все контакты, кроме последнего, т.к. у 
        последнего нет повторов, т.к после него вообще нет контактов. Цикл, что внутри него проходится по возможным 
        повторам. То есть по всем остальным контактам, начиная со того, что стоит после проверяемого. Далее условие
        Если совпадает Имя и Фамилия, то начинается схема с соединением. Я думал добавить туда еще совпадение телефона, 
        но если он будет одинаков, а имя и фамилия нет, то получится не круто наверное. Далее я прохожусь по двум 
        совпадающим контактам и если значение у первого не равно '', то есть ничему, то добавлем его в новый контакт, 
        иначе в новый контакт идет значение из дубликата. В конце обновляю телефонную книжку.
        """
        for contact in self.new_contacts_list[:-1]:
            for double_contact in self.new_contacts_list[index:]:
                if contact[0] == double_contact[0] and contact[1] == double_contact[1]:
                    new_contact = []
                    for item1, item2 in zip(contact, double_contact):
                        if item1 != '':
                            new_contact.append(item1)
                        else:
                            new_contact.append(item2)
                    nice_contact_list.remove(double_contact)
                    nice_contact_list.remove(contact)
                    nice_contact_list.append(new_contact)
            index += 1
        self.new_contacts_list = nice_contact_list


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='UTF-8') as f:  # открываем книгу
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list = PrettyContactsList(contacts_list)  # редактируем книгу
    contacts_list.correction_name()
    contacts_list.correction_number()
    contacts_list.correction_repetitions()

    with open("phonebook.csv", "w", encoding="UTF-8") as f:  # записываем все в новую книгу
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list.new_contacts_list)
