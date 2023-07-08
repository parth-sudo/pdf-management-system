import random
import string

def random_string_generator():
    string_letters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(string_letters) for _ in range(6))
    return random_string
