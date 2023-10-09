start_msg: str = "<b>Рад вас видеть, {}!</b>\n\n" \
                 "<b><i>Это MailEGuard</i> - программа, анализирующая содержание входящих писем с целью защиты от фишинга.</b>"

mainmenu: str = "<b>Для начала выберите провайдера, которого вы используете:</b>";

take_mail: str = "<b>Отлично, теперь отправьте адрес электронной почты.</b>";

wrong_email: str = "<b>Вы неккоректно указали email. Попробуйте еще раз или вернитесь к выбору провайдера.</b>";

take_passwd: str = "<b>Отлично, теперь отправьте пароль приложения.</b>\n\n<i>Как его узнать смотрите по ссылке ниже:</i>"

checking: str = "<b>Проверяем ящик, ожидайте...</b>";

wrong_check: str = "<b>Неправильный адрес или пароль! Попробуйте вновь, нажав на кнопку ниже:</b>";

success: str = ("<b>Прекрасно, защита запущена!</b>\n\nПо мере обнаружения чего-либо подозрительного "
                "вам будут приходить сообщения с предупреждениями. "
                "Чтобы остановить защиту введите команду /stopprotecting");

warning: dict = {
    "file": "<b>Предупреждение!</b>\n\nВам пришло письмо с адреса <i>{}</i>, которое содержит в себе файл. "
            "Перед открытием удостоверьтесь в том, что оно было отправлено с правильного домена. "
            "Файл потенциально может содержать вирусы, которые могут навредить вашему устройству.",
    "link": "<b>Предупреждение!</b>\n\nВам пришло письмо с адреса <i>{}</i>, которое содержит в себе ссылку. "
            "Перед открытием удостоверьтесь в том, что оно было отправлено с правильного домена "
            "и сама ссылка ведет на нужный сервис, а не поддельный сайт. "
            "Это можно определить по незаметным различиям в домене, "
            "например google.com (правильный) и googie.com (поддельный).",
    "fish": "<b>Предупреждение!</b>\n\nВам пришло письмо с адреса <i>{}</i>, которое, вероятно, является фишинговым. "
            "Наша система обнаружила в этом письме подозрительное поведение и ключевые слова, "
            "которые чаще всего используются мошенниками. Если вы планируете на него отвечать - "
            "обязательно проверьте почтовый домен на правильность. Никому не передавайте пароли, "
            "старайтесь не переходить по ссылкам и ни в коем случае не отправляйте данные банковского аккаунта."
};

stop_protecting: str = "<b>Защита остановлена!</b>\n\nЧтобы включить её заново просто введите команду /start и повторите вход заново."