

def adv_print(*args, max_line=False, in_file=False, start='', sep=" ", end="\n", file=sys.stdout, flush=False):
    all_str = start
    for item in args:
        all_str += str(item) + sep
    print(all_str)

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

