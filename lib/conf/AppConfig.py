import configparser
import logging


class AppConfig:

    def __init__(self):
        self._read_config()

    def _read_config(self):
        logging.info('The reading of the configuration file has begun')
        config = configparser.ConfigParser()
        config.read('config.ini')

        if 'BASE' not in config:
            logging.warning(f"Section 'BASE' not found in config file")
            raise ValueError("Section 'BASE' not found in config file")

        config_type = config['BASE'].get('config_type')

        self._is_create_key_file = config['BASE'].getboolean('is_create_key_file', fallback=False)
        if self._is_create_key_file:
            self._key_password = config['BASE'].get('key_password')

        if config_type not in config:
            logging.warning(f"Config type '{config_type}' not found in config file")
            raise ValueError(f"Config type '{config_type}' not found in config file")

        self._path_reports_for_phys = config[config_type].get('path_reports_for_phys')
        self._path_reports_for_legal = config[config_type].get('path_reports_for_legal')
        self._path_reports_for_mkd = config[config_type].get('path_reports_for_mkd')
        if self._path_reports_for_phys[-1] != '/':
            self._path_reports_for_phys += '/'
        if self._path_reports_for_legal[-1] != '/':
            self._path_reports_for_legal += '/'
        if self._path_reports_for_mkd[-1] != '/':
            self._path_reports_for_mkd += '/'

        self._sender_name = config[config_type].get('sender_name')
        self._mail_for_phys = config[config_type].get('mail_for_phys')
        self._mail_for_legal = config[config_type].get('mail_for_legal')

        self._is_delete_files = config[config_type].getboolean('is_delete_files', fallback=False)
        self._topic_of_letter = config[config_type].get('topic_of_letter')
        self._body_of_letter = config[config_type].get('body_of_letter')
        self._receivers_for_error_list = config[config_type].get('receivers_for_error_list')
        logging.info('Config file was successfully read')

    @property
    def is_create_key_file(self):
        return self._is_create_key_file

    @property
    def key_password(self):
        return self._key_password

    @property
    def path_reports_for_phys(self):
        return self._path_reports_for_phys

    @property
    def path_reports_for_legal(self):
        return self._path_reports_for_legal

    @property
    def path_reports_for_mkd(self):
        return self._path_reports_for_mkd

    @property
    def sender_name(self):
        return self._sender_name

    @property
    def mail_for_phys(self):
        return self._mail_for_phys

    @property
    def mail_for_legal(self):
        return self._mail_for_legal

    @property
    def is_delete_files(self):
        return self._is_delete_files

    @property
    def topic_of_letter(self):
        return self._topic_of_letter

    @property
    def body_of_letter(self):
        return self._body_of_letter

    @property
    def receivers_for_error_list(self):
        return self._receivers_for_error_list

    def print_all_info(self):
        print(f'{self._is_create_key_file}\n'
              # f'{self._key_password}\n'
              f'{self._path_reports_for_phys}\n'
              f'{self._path_reports_for_legal}\n'
              f'{self._sender_name}\n'
              f'{self._mail_for_phys}\n'
              f'{self._mail_for_legal}\n'
              f'{self._is_delete_files}\n'
              f'{self._topic_of_letter}\n'
              f'{self._body_of_letter}\n'
              f'{self._receivers_for_error_list}')
