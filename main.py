import telebot
from telebot import types
from auth_data import token
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart #позволяет прикреплять к письму разные форматы
import smtplib
import os
#from email.mime.base import MIMEBase
#from email import encoders
#from email.mime import message


sender = ""
password = ''
to_addr = ""
def send_email(to_addr, subject, text):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'plain'))

    # for file in files:
    #     attachment = open(file, 'rb')
    #     part = MIMEBase('application', 'octet-stream')
    #     part.set_payload((attachment).read())
    #     encoders.encode_base64(part)
    #     part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(file))
    #     msg.attach(part)

    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo(to_addr)
    server.login(sender, password)
    server.auth_plain()
    server.send_message(msg)

sender = "email_1"
password = '...'
to_addr1 = "email_2"
to_addr2 = "email_3"
to_addr3 = "email_4"
def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        if message.text == "Привет":
            bot.send_message(message.from_user.id, "Привет, вот список доступных почт:")

            keyboard = types.InlineKeyboardMarkup()   # Готовим кнопки

            key_mail_1 = types.InlineKeyboardButton(text='...', callback_data='1')   # По очереди готовим текст и обработчик
            keyboard.add(key_mail_1)   # И добавляем кнопку на экран

            key_mail_2 = types.InlineKeyboardButton(text='...', callback_data='2')   # По очереди готовим текст и обработчик
            keyboard.add(key_mail_2)   # И добавляем кнопку на экран

            key_mail_3 = types.InlineKeyboardButton(text='...', callback_data='3')   # По очереди готовим текст и обработчик
            keyboard.add(key_mail_3)   # И добавляем кнопку на экран

            bot.send_message(message.from_user.id, text='Выбери нужную почту, кому необходимо отправить письмо', reply_markup=keyboard)

        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши Привет")

        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

    @bot.message_handler(content_types=['document', 'photo'])  # добавлен обработчик для файлов
    def handle_files(message):

        try:
            file_id = message.document.file_id  # получаем id файла
            file_info = bot.get_file(file_id)  # получаем информацию о файле
            downloaded_file = bot.download_file(file_info.file_path)  # загружаем файл
            file_name = file_info.file_path
            with open(file_name, 'wb') as new_file:
                new_file.write(downloaded_file)  # сохраняем файл на сервере
            bot.reply_to(message, "Файл успешно сохранен")
            send_email(to_addr2, 'Hello', 'Hi', [file_name])  # отправляем файл по почте
            os.remove(file_name)  # удаляем файл после отправки

        except Exception as ex:
            bot.send_message(message.chat.id, "Что-то пошло не так: " + str(ex))  # отправляем сообщение об ошибке

    # Обработчик нажатий на кнопки
    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call, file_name=None):
        # Если нажали на одну из кнопок, то
        if call.data == "1":
            try:
                #send_email(to_addr1, 'Hello', 'Hi', [file_name])
                send_email(to_addr1, 'Hello', 'Hi')
            except Exception as ex:
                print(ex)
                bot.send_message(call.message.chat.id, "Что-то пошло не так...")

        elif call.data == "2":
            try :
                #send_email(to_addr2, 'Hello', 'Hi', [file_name])
                send_email(to_addr2, 'Hello', 'Hi')
            except Exception as ex:
                print(ex)
                bot.send_message(call.message.chat.id, "Что-то пошло не так...")

        elif call.data == "3":
            try:
                #send_email(to_addr3, 'Hello', 'Hi', [file_name])
                send_email(to_addr1, 'Hello', 'Hi')
            except Exception as ex:
                print(ex)
                bot.send_message(call.message.chat.id, "Что-то пошло не так...")
        else:
            bot.send_message(call.message.chat.id, "Проверь введенную команду")


    bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    telegram_bot(token)
