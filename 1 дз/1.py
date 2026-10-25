import string

SPECIAL_SYMBOLS = ['!', '@', '#', '$', '%', '&', '*', '+']
UPPERCASE_SYMBOLS = string.ascii_uppercase
LOWERCASE_SYMBOLS = string.ascii_lowercase
NUMBER_SYMBOLS = string.digits


def is_password_valid(password: str) -> bool:
    uppercase_symbol_check = False
    lowercase_symbol_check = False
    special_symbol_check = False
    number_symbol_check = False
    password_len = 0
    for s in password:
        if s in UPPERCASE_SYMBOLS:
            uppercase_symbol_check = True
        elif s in LOWERCASE_SYMBOLS:
            lowercase_symbol_check = True
        elif s in SPECIAL_SYMBOLS:
            special_symbol_check = True
        elif s in NUMBER_SYMBOLS:
            number_symbol_check = True
        else:
            return False
        password_len += 1
    if uppercase_symbol_check and lowercase_symbol_check and special_symbol_check and number_symbol_check and password_len >= 12:
        return True
    return False

if __name__ == '__main__':
    n = int(input())
    for _ in range(n):
        print('Valid' if is_password_valid(input()) else 'Invalid')
