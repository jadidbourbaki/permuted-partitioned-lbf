import random
import string

def random_string(max_len):
    """Generate a random string of random length up to max_len."""
    def generate_random_string(length):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for i in range(length))

    x_len = random.randint(1, max_len)
    return generate_random_string(x_len) 


def bytes_to_mb(bytes_value):
    """Converts bytes to megabytes."""
    return bytes_value / (1024 * 1024)