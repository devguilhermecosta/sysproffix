import random
import string


def generate_password() -> str:
    """
        generate a new password with length between 8 and 16 chars.
    """
    password_length = random.randint(8, 16)
    chars = string.ascii_letters + string.punctuation
    system = random.SystemRandom()
    new_password = ''.join(system.choices(chars, k=password_length))
    return new_password
