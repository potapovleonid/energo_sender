import logging

import lib.logging.Logger
import lib.archive.ArchiveCreator as Archiver
from lib.key import PasswordToKey
from lib.conf import AppConfig
from lib.mail import send_mail_utils

if __name__ == '__main__':
    try:
        lib.Logger().setup_logging()
    except Exception as e:
        print(f'Setup logging or config is failed. {e.__str__()}')
        exit()

    try:
        config = AppConfig.AppConfig()
    except Exception as e:
        logging.warning(f'Reading config wile has compete with error: {e.__str__()}')
        exit()

    if config.is_create_key_file:
        PasswordToKey.create_key_by_password(config.key_password)

    list_archive_paths_for_phys = Archiver.create_archives(config.path_reports_for_phys)
    error_phys_list = send_mail_utils.sending_files_to_one_mail_separately(config.sender_name,
                                                                           config.mail_for_phys,
                                                                           config.topic_of_letter,
                                                                           config.body_of_letter,
                                                                           list_archive_paths_for_phys)

    list_archive_paths_for_mkd = Archiver.create_archives(config.path_reports_for_mkd)
    error_mkd_list = send_mail_utils.sending_files_to_one_mail_separately(config.sender_name,
                                                                          config.mail_for_phys,
                                                                          config.topic_of_letter,
                                                                          config.body_of_letter,
                                                                          list_archive_paths_for_phys)

    list_archive_paths_for_legal = Archiver.create_archives(config.path_reports_for_legal)
    error_legal_list = send_mail_utils.sending_files_to_one_mail_separately(config.sender_name,
                                                                            config.mail_for_legal,
                                                                            config.topic_of_letter,
                                                                            config.body_of_letter,
                                                                            list_archive_paths_for_legal)

    # TODO Как реагируем на файлы без расширения .pdf?

    topic = 'Отчёт по рассылке'
    body = ''

    cnt_phys = len(list_archive_paths_for_phys) - len(error_phys_list)
    if error_phys_list:
        all_files = '<br>'.join(error_phys_list)
        body += f'Список архивов для <b>физ лиц</b> отправленных с ошибками:<br>{all_files}<br>'
    else:
        body += f'Все архивы для <b>физ лиц</b> были успешно отправлены {cnt_phys}<br><br><br>'

    cnt_legal = len(list_archive_paths_for_legal) - len(error_legal_list)
    if error_legal_list:
        all_files = '<br>'.join(error_legal_list)
        body += f'Список архивов для <b>юр лиц</b> отправленных с ошибками:<br>{all_files}<br>'
    else:
        body += f'Все архивы для <b>юр лиц</b> были успешно отправлены в количестве {cnt_legal}<br><br><br>'

    cnt_mkd = len(list_archive_paths_for_mkd) - len(error_mkd_list)
    if error_mkd_list:
        all_files = '<br>'.join(error_mkd_list)
        body += f'Список архивов для <b>мкд</b> отправленных с ошибками:<br>{all_files}'
    else:
        body += f'Все архивы для <b>мкд</b> были успешно отправлены в количестве {cnt_mkd}'

    send_mail_utils.send_email(config.sender_name,
                               config.receivers_for_error_list,
                               topic,
                               body,
                               None)
