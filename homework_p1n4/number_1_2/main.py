from homework_p1n4.number_1_2.application.salary import calculate_salary
from homework_p1n4.number_1_2.application.db.people import get_employees



if __name__ == '__main__':

    people_list = [get_employees(25, 5, 30000), get_employees(25, 5, 30000), get_employees(25, 5, 30000), get_employees(25, 5, 30000)]

    print(calculate_salary(people_list))