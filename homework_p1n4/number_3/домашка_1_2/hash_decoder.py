import hashlib

def string_hash_generator(file_path):
    file = open(file_path, "rb")
    for line in file:
        hash_string = hashlib.md5(line)
        hash_string = hash_string.hexdigest()
        yield hash_string

if __name__ == '__main__':
    my_generator = string_hash_generator("file.txt")

    for item in my_generator:
        print(item)
