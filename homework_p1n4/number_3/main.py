from homework_p1n4.number_3.домашка_1_1 import adv_print
from homework_p1n4.number_3.домашка_1_2 import hash_decoder
from homework_p1n4.number_3.домашка_1_3.decor import decorator

@decorator
def calc(num1, num2):
    return num1 + num2

if __name__ == "__main__":
    adv_print.adv_print(calc(92,80), max_line=2)

    decoder_file = hash_decoder.string_hash_generator('file.txt')
    for string in decoder_file:
        adv_print.adv_print(string)