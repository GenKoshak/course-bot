import telebot
import markups as m
from bot_phrases import BOT_PHRASES

bot = telebot.TeleBot(token, parse_mode=None)
is_running = False
name = []
bot_memory = []


@bot.message_handler(commands=['start', 'go'])
def start_handler(message):
    global name
    global is_running
    if not is_running:
        chat_id = message.chat.id
        text = message.text
        msg = bot.send_message(chat_id, 'Здравствуйте! Меня зовут Ирина. Я чат-бот компании Свобода Слова. '
                                        'Я могу подобрать вам программу по обучению английскому языку в '
                                        'нашей компании.'
                               , reply_markup=m.start_markup)
        bot.register_next_step_handler(msg, course_sign_up)
        print(chat_id)
        is_running = True

# def start_handler(message):
#     global name
#     global is_running
#     if not is_running:
#         chat_id = message.chat.id
#         text = message.text
#         if text == 'Закончить поиск':
#             name = []
#         if len(name) == 0:
#             msg = bot.send_message(chat_id, 'Здравствуйте! Меня зовут Ирина. Я чат-бот компании Свобода Слова. '
#                                             'Я могу подобрать вам программу по обучению английскому языку в '
#                                             'нашей компании.'
#                                    , reply_markup=m.start_markup)
#             bot.register_next_step_handler(msg, course_sign_up)
#             is_running = True
#         else:
#             msg = bot.send_message(chat_id, 'Итак, ' + str(name) + ', как давно вы изучаете английский?',
#                                    reply_markup=m.how_long_markup)
#             bot.register_next_step_handler(msg, how_regular)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def course_sign_up(message):
    chat_id = message.chat.id
    text = message.text
    msg = bot.send_message(chat_id, 'Хорошо! Ответьте на несколько вопросов. Как вас зовут?')
    bot.register_next_step_handler(msg, how_long)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def how_long(message):
    global name
    chat_id = message.chat.id
    text = message.text
    if text.isdigit():
        msg = bot.send_message(chat_id, 'Попробуйте ввести имя еще раз.')
        bot.register_next_step_handler(msg, how_long)
        return
    name = text.title()
    msg = bot.send_message(chat_id, 'Здравствуйте,  ' + name + '! Как давно вы изучаете английский?',
                           reply_markup=m.how_long_markup)
    bot.register_next_step_handler(msg, how_regular)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def how_regular(message):
    global is_running
    global bot_memory
    chat_id = message.chat.id
    text = message.text
    if text == "С детства":
        bot_memory.append('childhood')
        msg = bot.send_message(chat_id, 'Насколько регулярно вы занимаетесь/занимались английским языком?',
                               reply_markup=m.how_regular_markup)
        bot.register_next_step_handler(msg, regularity)
    elif text == "Последние несколько лет":
        bot_memory.append('few_years')
        msg = bot.send_message(chat_id, 'Насколько регулярно вы занимаетесь/занимались английским языком?',
                               reply_markup=m.how_regular_markup)
        bot.register_next_step_handler(msg, regularity)
    elif text == "Планирую начать":
        bot_memory.append('never')
        get_answer('beginner', chat_id, 3, m.finish_course_selection)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def regularity(message):
    global is_running
    chat_id = message.chat.id
    text = message.text
    if text == 'Очень редко':
        msg = bot.send_message(chat_id, 'Как бы вы охарактеризовали ваш нынешний'
                                        ' уровень владения английским языком?',
                               reply_markup=m.level_rare_markup)
        bot.register_next_step_handler(msg, level_rare)

    elif text == 'Регулярно занимаюсь самостоятельно/с преподавателем':
        msg = bot.send_message(chat_id, 'Как бы вы охарактеризовали ваш нынешний'
                                        ' уровень владения английским языком?',
                               reply_markup=m.level_rare_markup)
        bot.register_next_step_handler(msg, not_ready)
        is_running = False

    elif text == 'Никогда':
        msg = bot.send_message(chat_id, 'Как бы вы охарактеризовали ваш нынешний'
                                        ' уровень владения английским языком?',
                               reply_markup=m.level_rare_markup)
        bot.register_next_step_handler(msg, not_ready)
        is_running = False


@bot.message_handler(func=lambda message: True, content_types=['text'])
def level_rare(message):
    chat_id = message.chat.id
    text = message.text
    if text == 'Низкий. Малый словарный запас, разговорные навыки не развиты.':
        if 'childhood' in bot_memory:
            msg = bot.send_message(chat_id, 'Насколько хорошо вы знали английский язык в школе/университете?',
                                   reply_markup=m.lang_level_in_school)
            bot.register_next_step_handler(msg, lang_level_in_school)
        elif 'few_years' in bot_memory:
            msg = bot.send_message(chat_id, 'Для каких целей вы бы хотели продолжить изучать английский язык?',
                                   reply_markup=m.l_rare_goals)
            bot.register_next_step_handler(msg, l_rare_goals)
    elif text == 'Базовый. Испытываю трудности при использовании языка':
        if 'childhood' in bot_memory:
            msg = bot.send_message(chat_id, 'Для каких целей вы бы хотели продолжить изучать английский язык?',
                                   reply_markup=m.l_rare_goals)
            bot.register_next_step_handler(msg, not_ready)
        elif 'few_years' in bot_memory:
            msg = bot.send_message(chat_id, 'Для каких целей вы бы хотели продолжить изучать английский язык?',
                                   reply_markup=m.l_rare_goals)
            bot.register_next_step_handler(msg, not_ready)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def lang_level_in_school(message):
    global is_running
    chat_id = message.chat.id
    text = message.text
    if text == 'Скорее плохо, чем хорошо. Разговорной практики почти не было. ' \
               'Словарный запас был маленький, как и грамматика.':
        get_answer('beginner', chat_id, 3, m.finish_course_selection)
    elif text == 'Более-менее. Были какие-то знания грамматики и словарный запас.':
        msg = bot.send_message(chat_id, 'Для каких целей вы бы хотели продолжить изучать английский язык?',
                               reply_markup=m.lls_mid_goals)
        bot.register_next_step_handler(msg, lls_mid_goals)
    elif text == 'Очень хорошо! Был внушительный словарный запас и грамматика':
        msg = bot.send_message(chat_id, 'Для каких целей вы бы хотели продолжить изучать английский язык?',
                               reply_markup=m.lls_high_goals)
        bot.register_next_step_handler(msg, lls_high_goals)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def l_rare_goals(message):
    global is_running
    chat_id = message.chat.id
    text = message.text
    if text == 'По работе':
        get_answer('nolls_ce_business', chat_id, 4, m.finish_course_selection)
    elif text == 'Для учебы':
        get_answer('nolls_ce_study', chat_id, 2, m.finish_course_selection)
    elif text == 'Для путешествий':
        get_answer('nolls_ce_travel', chat_id, 4, m.finish_course_selection)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def lls_mid_goals(message):
    global is_running
    chat_id = message.chat.id
    text = message.text
    if text == 'Для учебы':
        get_answer('ee_study', chat_id, 4, m.finish_course_selection)
    elif text == 'По работе':
        get_answer('ee_business', chat_id, 4, m.finish_course_selection)
    elif text == 'Для путешествий':
        get_answer('ee_travel', chat_id, 4, m.finish_course_selection)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def lls_high_goals(message):
    global is_running
    chat_id = message.chat.id
    text = message.text
    if text == 'Для учебы':
        get_answer('ce_study', chat_id, 4, m.finish_course_selection)
    elif text == 'По работе':
        get_answer('ce_business', chat_id, 4, m.finish_course_selection)
    elif text == 'Для путешествий':
        get_answer('ce_travel', chat_id, 4, m.finish_course_selection)


def not_ready(message):
    global name
    global is_running
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'У меня больше нет вопросов, как и предложений. Скоро я буду значительно '
                                    'умнее и способнее, а пока предлагаю повторить',
                           reply_markup=m.finish_course_selection)
    bot.register_next_step_handler(msg, start_handler)
    is_running = False


def get_answer(bot_phrase, chat_id, number, reply_markup):
    global is_running
    answer = BOT_PHRASES[bot_phrase]
    for i in range(0, number):
        msg = bot.send_message(chat_id, answer[i], reply_markup=reply_markup)
    bot.register_next_step_handler(msg, start_handler)
    is_running = False
    return msg


if __name__ == "__main__":
    bot.infinity_polling()
# bot.polling(none_stop=True)
