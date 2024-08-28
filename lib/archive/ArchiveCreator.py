import logging

from cryptography.fernet import Fernet
import datetime
import os
import pyzipper


def _load_password():
    with open('./key.key', 'rb') as key_file:
        key = key_file.read()

    with open('./encrypted_password.bin', 'rb') as encrypted_file:
        ciphered_password = encrypted_file.read()

    cipher_suite = Fernet(key)
    password = cipher_suite.decrypt(ciphered_password).decode()

    return password


def create_archives(path):
    current_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    current_date = current_date.__str__()
    file_path = path + current_date
    password = _load_password()
    all_files = [file for file in os.listdir(file_path) if file.endswith('.pdf')]

    list_archive_paths = []

    for file in all_files:
        zip_archive_name = f'{file_path}/{file}.zip'
        logging.info(f'File {zip_archive_name} has started archiving')

        if os.path.exists(zip_archive_name):
            os.remove(zip_archive_name)

        try:
            with pyzipper.AESZipFile(zip_archive_name,
                                     'w',
                                     compression=pyzipper.ZIP_LZMA,
                                     encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(password.encode())
                zf.write(os.path.join(file_path, file), arcname=file)
                logging.info(
                    f'The file {file} has been successfully added to the archive {zip_archive_name} with a password.')
                list_archive_paths.append(zip_archive_name)
        except Exception as e:
            logging.warning(f'Archiving {file} has complete with an error {e.__str__()}')
    return list_archive_paths
