import string
import random

def generate_secret_key(length=50):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

secret_key = generate_secret_key()
print(secret_key)