"""

MailEGuard Class
Licence - GNU GPLv2 ECHO'S DEVELOPMENT (https://t.me/echoscode)

"""



""" IMPORTS """
import imaplib;
import email;
from email.header import decode_header;
import base64;
from time import sleep;
from database import Database;
from login import bot;
import time;
from messages import warning;



class GuardException (Exception):
    def __init__ (self, text: str) -> None:
        self.text = text;



class Guard:
    def __init__ (self, email: str, password: str, server_name: str, rating: int) -> None:
        self.__servers_imap: dict = {
            "rambler": ("imap.rambler.ru", 993),
            "mail.ru": ("imap.mail.ru", 993),
            "yandex": ("imap.yandex.ru", 993)
        };
        self.__email: str = email;
        self.__password: str = password;
        try:
            self.__imap_host = imaplib.IMAP4_SSL(self.__servers_imap[server_name.lower()][0]);
            self.__imap_host.login(self.__email, self.__password);
        except Exception as ex:
            raise GuardException(f"Login failed. Check your email and password.\n\nimap error text: {ex}");
        self.__rating: int = rating;

    def get_messages_count (self) -> int:
        status, messages = self.__imap_host.select("INBOX");
        return int(messages[0]);

    def read_message (self, number: int) -> tuple:
        result, mail = self.__imap_host.fetch(str(number), '(RFC822)');
        message = email.message_from_bytes(mail[0][1]);
        letter_from = message["Return-path"];
        file_check: bool = False;
        msg_text: str = "";
        for part in message.walk():
            if (part.get_content_disposition() == 'attachment'):
                file_check = True;
            else:
                pass;

            if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
                msg_text = base64.b64decode(part.get_payload()).decode();
            else:
                continue;
        return letter_from, msg_text, file_check;

    def check_message (self, message: str) -> tuple:
        english_alphabet: str = 'abcdefghijklmnopqrstuvwxyz';
        russian_alphabet: str = "абвгдеёжзиклмнопрстуфхцчшщъыьэюя";
        ban_words: tuple = ("парол", "деньги", "поддержк", "средства", "средств",
                            "взлом", "атака", "атаке", "карт",
                            "данные", "оплат", "розыгрыш", "ссылк",
                            "раздач", "приз", "отправь", "аккаунт",
                            "заблокир", "доставлено", "объем", "ящик", "безопасн", "финанс",
                            "штраф", "вирус", "банк", "счет", "счёт", "чёрн", "черн", "qr", "выигр", "лотер");
        rating: int = 100;
        message_to_analytics: str = message.lower();
        for word in ban_words:
            if (word in message_to_analytics):
                rating -= 5;
            else:
                continue;
        fish_text: bool = True if (rating <= self.__rating) else False;
        for word in message_to_analytics.split(" "):
            stat_en: bool = False;
            stat_ru: bool = False;

            for char in word:
                if (char in english_alphabet):
                    stat_en = True;
                elif (char in russian_alphabet):
                    stat_ru = True;
                else:
                    continue;

            if (stat_en and stat_ru):
                fish_text = True;
                break;
            else:
                continue;

        link: bool = True if ("http" in message_to_analytics) else False;
        return fish_text, link;

    def start_protecting (self, chat_id: int) -> None:
        message_count: int = self.get_messages_count();
        while (True):
            database = Database(chat_id);
            if (database.get_threadstatus()):
                del database;
            else:
                return;

            now: int = self.get_messages_count();
            print(now)
            if (now > message_count):
                try:
                    email_address, text, file_status = self.read_message(now);
                except Exception:
                    time.sleep(5);
                    continue;
                if (file_status):
                    bot.send_message(chat_id, text=warning["file"].format(email_address), parse_mode="html");
                    message_count = now;
                    continue;
                fish_status, link = self.check_message(text);
                if (link):
                    bot.send_message(chat_id, text=warning["link"].format(email_address), parse_mode="html");
                elif (fish_status):
                    bot.send_message(chat_id, text=warning["fish"].format(email_address), parse_mode="html");
                time.sleep(5);
                message_count = now;
            else:
                time.sleep(5);
                continue;
