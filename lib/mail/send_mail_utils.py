import logging
import smtplib  # Импортируем библиотеку по работе с SMTP
import os  # Функции для работы с операционной системой, не зависящие от используемой операционной системы

# Добавляем необходимые подклассы - MIME-типы
import mimetypes  # Импорт класса для обработки неизвестных MIME-типов, базирующихся на расширении файла
from email import encoders  # Импортируем энкодер
from email.mime.base import MIMEBase  # Общий тип
from email.mime.text import MIMEText  # Текст/HTML
from email.mime.image import MIMEImage  # Изображения
from email.mime.audio import MIMEAudio  # Аудио
from email.mime.multipart import MIMEMultipart  # Многокомпонентный объект


def sending_files_to_one_mail_separately(sender_name, addr_to, msg_subj, msg_text, file_list):
    error_message = []
    for file in file_list:
        res = send_email(sender_name, addr_to, msg_subj, msg_text, [file])
        if not res:
            error_message.append(file)
    return error_message


def send_email(sender_name, addr_to, msg_subj, msg_text, files):
    try:
        logging.getLogger().info(f"Start sending mail with list files: {files.__str__()}")
        addr_from = sender_name  # Отправитель
        # password  = ""                                  # Пароль

        msg = MIMEMultipart()  # Создаем сообщение
        msg['From'] = addr_from  # Адресат
        msg['To'] = addr_to  # Получатель
        msg['Subject'] = msg_subj  # Тема сообщения

        body = msg_text  # Текст сообщения
        msg.attach(MIMEText(body, 'html'))  # Добавляем в сообщение текст

        if files is not None:
            _process_attachment(msg, files)

        # ======== Этот блок настраивается для каждого почтового провайдера отдельно ===============================================
        server = smtplib.SMTP('10.0.103.2', 25)  # Создаем объект SMTP
        # server.starttls()                                      # Начинаем шифрованный обмен по TLS
        # server.set_debuglevel(True)                            # Включаем режим отладки, если не нужен - можно закомментировать
        # server.login(addr_from, password)                       # Получаем доступ
        server.send_message(msg)  # Отправляем сообщение
        server.quit()  # Выходим
        logging.info("The mail sent successfully")
        return True
        # ==========================================================================================================================
    except Exception as ve:
        logging.getLogger().warning(f"The mail wasn't send {files}\nException: " + ve.__str__())
        return False


def _process_attachment(msg, files):  # Функция по обработке списка, добавляемых к сообщению файлов
    for f in files:
        if os.path.isfile(f):  # Если файл существует
            # logging.info("File was find: " + f) # Раскомментировать при необходимости логирования
            _attach_file(msg, f)  # Добавляем файл к сообщению
            continue
        elif os.path.exists(f):  # Если путь не файл и существует, значит - папка
            # logging.info("File is directory: " + f)    # Раскомментировать при необходимости логирования
            directory = os.listdir(f)  # Получаем список файлов в папке
            for file in directory:  # Перебираем все файлы и...
                _attach_file(msg, f + "/" + file)  # ...добавляем каждый файл к сообщению
                continue
        # logging.warning("File not found" + f.__str__())


def _attach_file(msg, filepath):  # Функция по добавлению конкретного файла к сообщению
    filename = os.path.basename(filepath)  # Получаем только имя файла
    ctype, encoding = mimetypes.guess_type(filepath)  # Определяем тип файла на основе его расширения
    if ctype is None or encoding is not None:  # Если тип файла не определяется
        ctype = 'application/octet-stream'  # Будем использовать общий тип
    maintype, subtype = ctype.split('/', 1)  # Получаем тип и подтип
    if maintype == 'text':  # Если текстовый файл
        with open(filepath) as fp:  # Открываем файл для чтения
            file = MIMEText(fp.read(), _subtype=subtype)  # Используем тип MIMEText
            fp.close()  # После использования файл обязательно нужно закрыть
    elif maintype == 'image':  # Если изображение
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':  # Если аудио
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:  # Неизвестный тип файла
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)  # Используем общий MIME-тип
            file.set_payload(fp.read())  # Добавляем содержимое общего типа (полезную нагрузку)
            fp.close()
            encoders.encode_base64(file)  # Содержимое должно кодироваться как Base64
    file.add_header('Content-Disposition', 'attachment', filename=filename)  # Добавляем заголовки
    msg.attach(file)  # Присоединяем файл к сообщению
