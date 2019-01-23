#задание 2
class Contact():
    contact_list = []

    def __init__(self, name, surname, phone_number, special_contact = False, **kwargs):
        contact = {
            name: name,
            surname: surname,
            phone_number: phone_number,
            special_contact: special_contact,

        }
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                self.contact[key] = value
        self.contact_list.append(contact)

    def contact_print(self):
        for cont in self.contact_list:
            print('Имя: ', self.cont['name'])
            print('Фамилия: ', self.cont['surname'])
            print('Телефон: ', self.cont['phone_number'])
            print('В избранных: ', self.cont['special_contact'])
            print('Дополнительная информация: ')
            print('    telegram: ', self.cont['telegram'])
            print('    email: ', self.cont['email'])

    def append(self, name, surname, phone_number, special_contact=False, **kwargs):
        contact = {
            name: name,
            surname: surname,
            phone_number: phone_number,
            special_contact: special_contact,

        }
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                self.contact[key] = value
        self.conts.append(contact)

    def delete(self, number):
        index = 0
        for cont in self.contact_list:
            if number == cont['phone_number']:
                self.contact_list.pop(index)
            index += 1

    #задание 3
    def find_special(self):
        for cont in self.contact_list:
            if cont['special_contact'] == True:
                self.contact_print()

    def find_name(self, name, surname):
        for cont in self.contact_list:
            if cont['name'] == name and cont['surname'] == surname:
                self.contact_print()
