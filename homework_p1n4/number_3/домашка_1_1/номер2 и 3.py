
# задание 1

class Contact():
    def __init__(self, name, surname, phone_number, special_contact = False, **kwargs):
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.special_contact = special_contact
        self.additional_information = kwargs

    def __str__(self):
        print("Имя:", self.name)
        print("Фамилия:", self.surname)
        print("Телефон:", self.phone_number)

        if self.special_contact == False:
            print("В избранных: нет")
        else:
            print("В избранных: да")

        print("Дополнительная информация:")
        for key, value in self.additional_information.items():
            print("\t\t", key, " : ", value, sep="")

        return ''

jhon = Contact('Jhon', 'Smith', '+71234567809', telegram='@jhony', email='jhony@smith.com')
print(jhon)


#задание 2

class PhoneBook():

    def __init__(self, name):
        self.name = name
        self.contacts_list = []

    def contacts_print(self):
        for contact in self.contacts_list:
            print(contact)

    def append_phone(self, contact):
        if isinstance(jhon, Contact):
            self.contacts_list.append(contact)
        else:
            print("Ошибка, нужен класс, типа Contact")

    def delete(self, number):
        index = 0
        for contact in self.contacts_list:
            if number == contact.phone_number:
                self.contacts_list.pop(index)
            index += 1

    #задание 3
    def find_special(self):
        for cont in self.contacts_list:
            if cont.special_contact:
                print(cont)

    def find_name(self, name, surname):
        for cont in self.contacts_list:
            if cont.name == name and cont.surname == surname:
                print(cont)

a = PhoneBook("Книжка")
a.append_phone(jhon)
a.contacts_print()
a.delete('+71234567809')
a.contacts_print()
