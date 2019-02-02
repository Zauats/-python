import datetime, sys

# задание 2
def path_decorator(file_path):
    def decorator(old_function):
        def new_function(*args, **kwargs):
            data = old_function(*args, **kwargs)
            with open(file_path, 'w', encoding='UTF-8') as f:
                f.write('время вызова функции: ' + str(datetime.datetime.now()) + '\n')
                f.write('Имя функции: ' + str(old_function.__name__) + '\n')
                f.write('Аргументы функции: ' + str(args) + str(kwargs) + '\n')
                f.write('Возвращаемое значение: ' + str(data) + '\n')
            return data
        return new_function
    return decorator



# задание 1
def decorator(old_function):
    def new_function(*args, **kwargs):
        data = old_function(*args, **kwargs)
        with open('file.txt', 'w', encoding='UTF-8') as f:
            f.write('время вызова функции: ' + str(datetime.datetime.now()) + '\n')
            f.write('Имя функции: ' + str(old_function.__name__) + '\n')
            f.write('Аргументы функции: ' + str(args) + str(kwargs) + '\n')
            f.write('Возвращаемое значение: ' + str(data) + '\n')
        return data
    return new_function


# задание 3
@path_decorator('file.txt')
def adv_print(*args, max_line=False, in_file=False, start='', sep=" ", end="\n", file=sys.stdout, flush=False):
    all_str = start
    for item in args:
        all_str += str(item) + sep

    if max_line == False:
        print(all_str, end=end, sep='', file=file, flush=flush)

    else:
        start_index = 0
        while max_line < len(all_str) - start_index:
            print(all_str[start_index : max_line + start_index], sep='', file=file, flush=flush)
            start_index += max_line

        print(all_str[start_index:], end=end, sep='', file=file, flush=flush)

    if in_file:
        file = input('введите путь к файлу')
        with open(file, 'w')  as f:
            for obj in args:
                f.write(obj)

adv_print(123, max_line=2)

