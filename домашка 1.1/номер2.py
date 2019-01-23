class Contact():
    def __init__(self, name, surname, phone_number, special_contact = False, **kwargs):
        self.name = name
        self.surname = surname
        self.phone_number = phone_number
        self.special_contact = special_contact
        if len(kwargs) > 0:
            for key, value in kwargs.items():
                self.key = value

        