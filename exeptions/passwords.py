class PasswordError(Exception):
    pass


class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


def check_password(st):
    lst_bad = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "йцукенгшщзхъ", "фывапролджэё", "ячсмитьбю"]
    if len(st) < 9:
        raise LengthError
    count_up = 0
    count_low = 0
    count_num = 0
    for i in st:
        if i.isupper():
            count_up += 1
        elif i.islower():
            count_low += 1
        elif i.isdigit():
            count_num += 1
    if count_low == 0 or count_up == 0:
        raise LetterError
    if count_num == 0:
        raise DigitError
    st_low = st.lower()
    for i in lst_bad:
        for j in range(len(i) - 2):
            if i[j: j + 3] in st_low:
                raise SequenceError
    return 'ok'


try:
    print(check_password("U3UшHЪnDЧ5yш.yмЯpH"))
except Exception as error:
    print(error.__class__.__name__)
'''try:
    print(check_password("G7FgTU0bwТuio"))
except Exception as error:
    print(error.__class__.__name__)
try:
    print(check_password("GБвИНddифпГxFGH"))
except Exception as error:
    print(error.__class__.__name__)
try:
    print(check_password("41157082"))
except Exception as error:
    print(error.__class__.__name__)'''

