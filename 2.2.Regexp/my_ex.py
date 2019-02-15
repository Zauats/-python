import re
from pprint import pprint


import csv
with open("phonebook_raw.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
nice_contacts_list = [] #новый список контактов
for people in contacts_list[1:]:
    people_list = str(people[0] + ' ' + people[1] + ' ' + people[2]).strip().split(' ')
    """объеденяю первые три элемента списка в одну строку. 
    Получается строка с ФИО в Таком виде: 'Имя Фамилия Отчество'
    Затем сразу убираю крайние пробельные символы и разбиваю по пробелу. Получается список такого вида: [Имя, Фамилия, Отчество]
    """
    if len(people_list) == 2:
        people_list.append('') # на стучай, если в записях была только имя и фамилия, что бы не ломать структуру.

    people_list.extend(people[3:]) # добавляю остальные данные, что были в изначальном списоке


    people_list[5] = re.sub('[\W, \.]', '', people_list[5]) #убираю из телефонного номера все, что мешает, что бы привести к одному формату
    # print(people_list[5])
    if len(people_list[5]) > 0:
        people_number = '+7(' + people_list[5][1:4] + ')' + people_list[5][4:7] + '-' + people_list[5][7:9] + '-' + people_list[5][9:11]
        if len(people_list[5]) > 12:
            people_number += ' (' + people_list[5][11:14] + '.' + people_list[5][14:18] + ')'
        people_list[5] = people_number

    nice_contacts_list.append(people_list)

contact_index = 0
for contact in nice_contacts_list:
    coincidence = False
    contact_index2 = 0
    for people in nice_contacts_list:
        if (contact[0] == people[0] and contact[1] == people[1]) and not coincidence:
            coincidence = True
            continue

        if contact[0] == people[0] and contact[1] == people[1]:
            nice_contacts_list.remove(contact)
            nice_contacts_list.remove(people)
            item_index = 0
            new_contact = []
            for item in contact:
                if item == '':
                    new_contact.append(people[item_index])
                else:
                    new_contact.append(item)
                item_index += 1
            nice_contacts_list.remove(contact)
            nice_contacts_list.remove(people)
            nice_contacts_list.append(new_contact)


    coincidence = False
    contact_index += 1

pprint(nice_contacts_list)






# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(contacts_list)

