import secrets
import string

def generate_token(length):
    characters = string.ascii_letters + string.digits

    token = ''.join(secrets.choice(characters) for _ in range(length))

    return token

