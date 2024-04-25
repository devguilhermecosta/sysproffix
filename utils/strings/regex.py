import re


def strong_password(password: str) -> bool:
    """
        The password must have:
        - 8 characters at least
        - 1 lowercase letter
        - 1 uppercase letter
        - 1 number
    """
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    return True if regex.match(password) else False


# TODO criar os testes
