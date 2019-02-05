


def calculate_salary(people_list):
    salary = 0
    for people in people_list:
        salary += people.salary
    return salary
