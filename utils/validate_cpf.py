import re


def clean_cpf(cpf: str) -> str:
    return re.sub(r'\D', '', cpf)


def verify_length(value: iter, length: int = 11) -> bool:
    return len(value) == length


def is_repeated(value: str) -> bool:
    return value[0] * len(value) == value


def get_digit(cpf: str) -> str:

    length = len(cpf) + 1

    total_sum = 0
    for cpf_digit, multiplier in zip(cpf, range(length, 1, -1)):
        total_sum += int(cpf_digit) * multiplier

    operation = 11 - (total_sum % 11)

    return str(operation) if operation <= 9 else '0'


def get_first_digit(sequence: str) -> str:
    return get_digit(sequence[:9])


def get_second_digit(sequence: str) -> str:
    return get_digit(sequence[:10])


def validate_cpf(cpf: str) -> bool:

    cleanned_cpf = clean_cpf(cpf)

    if not verify_length(cleanned_cpf):
        return False

    if is_repeated(cleanned_cpf):
        return False

    first_digit = get_first_digit(cleanned_cpf)
    second_digit = get_second_digit(cleanned_cpf + first_digit)
    generated_cpf = cpf[:-2] + first_digit + second_digit

    return True if cpf == generated_cpf else False
