

class employees():
    def __init__(self, age, experience, salary):
        self.age = age
        self.experience = experience
        self.salary = salary

def get_employees(age, experience, salary):
    return employees(age, experience, salary)