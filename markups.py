from telebot import types
from bot_phrases import BOT_PHRASES


def define_markup(markup_name, width, resize):
    l = []
    for v in BOT_PHRASES[markup_name]:
        l.append(v)
    markup = types.ReplyKeyboardMarkup(row_width=width, resize_keyboard=resize, one_time_keyboard=True)
    markup_name = markup
    if len(l) == 1:
        markup_name.add(types.KeyboardButton(l[0]))
    elif len(l) == 2:
        markup_name.add(types.KeyboardButton(l[0]), types.KeyboardButton(l[1]))
    elif len(l) == 3:
        markup_name.add(types.KeyboardButton(l[0]), types.KeyboardButton(l[1]), types.KeyboardButton(l[2]))
    elif len(l) == 4:
        markup_name.add(types.KeyboardButton(l[0]), types.KeyboardButton(l[1]),
                        types.KeyboardButton(l[2]), types.KeyboardButton(l[3]))
    return markup_name


start_markup = define_markup('start_markup', 1, True)
how_long_markup = define_markup('how_long_markup', 2, True)

how_regular_markup = define_markup('how_regular_markup', 1, True)

level_rare_markup = define_markup('level_rare_markup', 1, True)

lang_level_in_school = define_markup('lang_level_in_school', 1, False)

l_rare_goals = define_markup('l_rare_goals', 2, True)

lls_mid_goals = define_markup('lls_mid_goals', 2, True)

lls_high_goals = define_markup('lls_high_goals', 2, True)

finish_course_selection = define_markup('finish_course_selection', 1, True)
