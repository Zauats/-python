from math import inf


# номер 1
# По-моему я здесь что-то намудрил, можно сделать все гораздо проще.
def adv_print (*args, max_line=inf, in_file=False, start='', sep=' ', end='\n',):
    print(start, end='')
    for obj in args:
        obj = str(obj)
        if max_line != inf:
                # print(obj, end='')
            1+1
        else:

            str_min_index = 0
            str_max_index = max_line
            loop = True

            while loop:
                if len(obj) < str_min_index:
                    loop = False
                elif len(obj) < str_max_index:
                    print(obj[str_min_index:])
                    loop = False
                else:
                    # print(obj[str_min_index:str_max_index], end='')
                    str_max_index +=max_line
                    str_min_index +=max_line


        print(sep, end='')

    print(end, end='')

    if in_file:
        file = input('введите путь к файлу')
        with open(file, 'w')  as f:
            for obj in args:
                f.write(obj)
