import re
from pprint import pprint


import csv
with open("phonebook_raw.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ


class PrettyContactsList():
    def __init__(self, contact_list):
        self.old_contacts_list = contact_list
        self.new_contacts_list = []

    def correction_name(self): #корректирует ФИО
        nice_contacts_list = []  # список, в котором будут новые, исправленные контакты
        for people in self.old_contacts_list[1:]:
            people_list = str(people[0] + ' ' + people[1] + ' ' + people[2]).strip().split(' ')
            """объеденяю первые три элемента списка в одну строку. 
            Получается строка с ФИО в Таком виде: 'Имя Фамилия Отчество'
            Затем сразу убираю крайние пробельные символы и разбиваю по пробелу. Получается список такого вида: 
            [Имя, Фамилия, Отчество]
            """
            if len(people_list) == 2:
                people_list.append('')  # на стучай, если в записях была только имя и фамилия, что бы не ломать структуру.
            people_list.extend(people[3:])  # добавляю остальные данные, что были в изначальном списоке
            nice_contacts_list.append(people_list) # добавляю список со всеми контаками
        self.new_contacts_list = nice_contacts_list # обновляю контактную книгу

    def correction_number(self): #Корректирует номер
        nice_contacts_list = [] # список, в котором будут новые, исправленные контакты
        for people_list in self.new_contacts_list:
            people_list[5] = re.sub('[\W, \.]', '', people_list[5])
            # убираю из телефонного номера все, что мешает, что бы привести к одному формату
            if len(people_list[5]) > 0: # Условие, проверяющее на то, что телефонный номер у контакта есть
                people_number = '+7(' + people_list[5][1:4] + ')' + people_list[5][4:7] + '-' + people_list[5][7:9] + '-' + \
                                people_list[5][9:11]
                # создаю новый телефонный номер, в правильном формате

                if len(people_list[5]) > 12: #проверяю, есть ли добавочный номер
                    people_number += ' (' + people_list[5][11:14] + '.' + people_list[5][14:18] + ')'
                    #Делаю с добавочнфм номером, то же, что и с оттальным номером
                people_list[5] = people_number # заменяю старый стандарт номера на новый

            nice_contacts_list.append(people_list) # добавляю контакт с новым номером в книгу
        self.new_contact_list = nice_contacts_list # обновляю контактную книгу

    def correction_repetitions(self): # Убирает повторы
        new_contacts = [] # список с новыми контактами, состоящими из двух старых
        for contact in self.new_contacts_list: # Походимся по всем контактам
            coincidence = False # т.к первое совпадение это не повторяющийся контакт, то его заменять не нужно
            for people in self.new_contacts_list: # проходимся по контактам еще раз и ищем совпадения
                if (contact[0] == people[0] and contact[1] == people[1]) and not coincidence:
                    # условие, определяющее было ли первое совпадение или нет
                    coincidence = True # если первое совпадение было, то ставим то, что оно было.
                    # Если это не первое совпадение, то условие сюда не попадет
                    continue

                if contact[0] == people[0] and contact[1] == people[1] and coincidence: # проверка на второе совпадение
                    item_index = 0 # индекс значения контакта
                    new_contact = [] # новый контакт, состоящий из двух старых
                    for item in contact:
                        if item == '':
                            new_contact.append(people[item_index])
                        else:
                            new_contact.append(item)
                        item_index += 1
                    # в этом цикле проходимся по всем значениям контакта номер один и если там есть пробелы,
                    # заполняем их значениями из контакта 2
                    self.new_contact_list.remove(contact)
                    self.new_contacts_list.remove(people)
                    # удаляю старые два контакта
                    new_contacts.append(new_contact) # добавляю новый контакт в отдельный список

        self.new_contacts_list.extend(new_contacts) # добавляю новые контакты в записную книгу


contacts_list = PrettyContactsList(contacts_list)
contacts_list.correction_name()
contacts_list.correction_number()
contacts_list.correction_repetitions()

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="UTF-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(contacts_list.new_contacts_list)

