from cryptography.fernet import Fernet


def create_key_by_password(clear_password):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    password = clear_password.encode()

    ciphered_password = cipher_suite.encrypt(password)
    with open('key.key', 'wb') as key_file:
        key_file.write(key)
    with open('encrypted_password.bin', 'wb') as encrypted_file:
        encrypted_file.write(ciphered_password)


class PasswordToKey:

    def __init__(self):
        super().__init__()
