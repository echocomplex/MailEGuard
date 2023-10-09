"""

MailEGuard by echo complex
Licence - GNU GPLv2 ECHO'S DEVELOPMENT (https://t.me/echoscode)

"""

print("Starting...");


""" IMPORTS """
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton;
from buttons import *;
from messages import *;
from guard import Guard, GuardException;
from database import Database;
from threading import Thread;
from login import bot;



@bot.message_handler()
def start (message) -> None:
    database = Database(message.chat.id);
    database.add_user();
    del database;

    markup = InlineKeyboardMarkup()
    cont = InlineKeyboardButton(text="Продолжить", callback_data="mainmenu");
    markup.add(cont);
    bot.send_message(message.chat.id, text=start_msg.format(message.chat.first_name),
                     parse_mode="html", reply_markup=markup);

@bot.message_handler(commands=["stopprotecting"])
def stopprotecting (message) -> None:
    database = Database(message.chat.id);
    database.add_user();
    database.set_threadstatus(0);
    del database;

    bot.send_message(message.chat.id, text=stop_protecting,
                     parse_mode="html");




@bot.callback_query_handler(func=lambda call: True)
def inline (call) -> None:
    database = Database(call.message.chat.id);
    database.add_user();
    del database;

    if (call.data == "mainmenu"):
        markup = InlineKeyboardMarkup();
        for text, callback in choose_client.items():
            btn = InlineKeyboardButton(text=text, callback_data=callback);
            markup.add(btn);
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=mainmenu,
                              parse_mode="html", reply_markup=markup);
    else:
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=take_mail, parse_mode="html");
        bot.register_next_step_handler(msg, take_email, call.data);



def take_email (message, provider: str) -> None:
    database = Database(message.chat.id);
    database.add_user();
    del database;

    email: str = message.text;
    markup = InlineKeyboardMarkup();
    if (email.count("@") == 1):
        pass;
    else:
        btn = InlineKeyboardButton(text="К выбору провайдера", callback_data="mainmenu");
        markup.add(btn);
        msg = bot.send_message(message.chat.id, text=wrong_email, parse_mode="html",
                               reply_markup=markup);
        bot.register_next_step_handler(msg, take_email, provider);
        return;
    btn = InlineKeyboardButton(text="Как узнать пароль для почтового приложения?",
                               url="https://telegra.ph/Kak-uznat-parol-dlya-pochtovogo-prilozheniya-10-09");
    markup.add(btn);
    msg = bot.send_message(message.chat.id, text=take_passwd,
                           parse_mode="html", reply_markup=markup);
    bot.register_next_step_handler(msg, take_password, email, provider);

def take_password (message, email: str, provider: str) -> None:
    database = Database(message.chat.id);
    database.add_user();
    database.set_threadstatus(1);
    del database;

    password: str = message.text;
    chat_id: int = message.chat.id;
    bot.send_message(chat_id, text=checking, parse_mode="html");
    try:
        guard_unit = Guard(email, password, provider, 80);
    except GuardException:
        markup = InlineKeyboardMarkup();
        back = InlineKeyboardButton(text="Ещё раз", callback_data="mainmenu");
        markup.add(back);
        bot.send_message(chat_id=message.chat.id, text=wrong_check, parse_mode="html",
                         reply_markup=markup);
        return;
    Thread(target=guard_unit.start_protecting, args=(message.chat.id,)).start();
    bot.send_message(chat_id=message.chat.id, text=success, parse_mode="html");





if (__name__ == "__main__"):
    print("Bot MailEGuard is started and ready to work.");
    bot.polling(none_stop=True, interval=0);
