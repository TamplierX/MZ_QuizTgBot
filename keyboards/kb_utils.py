from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)

from services.variables import BOT_NAME
from services.results import RESULTS


start_quiz_btn = InlineKeyboardButton(
    text='Начать викторину',
    callback_data='start_quiz'
)

about_btn = InlineKeyboardButton(
    text='Узнать больше',
    callback_data='about'
)

zoo_url_btn = InlineKeyboardButton(
    text='Сайт "Московского зоопарка"',
    url='https://moscowzoo.ru'
)

answer_1_btn = InlineKeyboardButton(
    text='1',
    callback_data='1'
)

answer_2_btn = InlineKeyboardButton(
    text='2',
    callback_data='2'
)

answer_3_btn = InlineKeyboardButton(
    text='3',
    callback_data='3'
)

answer_4_btn = InlineKeyboardButton(
    text='4',
    callback_data='4'
)

guardianship_url_btn = InlineKeyboardButton(
    text='Программа опеки',
    url='https://moscowzoo.ru/about/guardianship'
)

ask_btn = InlineKeyboardButton(
    text='Задать вопрос',
    callback_data='ask'
)

feedback_btn = InlineKeyboardButton(
    text='Оставить отзыв',
    callback_data='feedback'
)

start_quiz_again_btn = InlineKeyboardButton(
    text='Попробовать ещё раз',
    callback_data='start_quiz'
)

cancel_btn = InlineKeyboardButton(
    text='Отмена',
    callback_data='cancel'
)

share_btn = InlineKeyboardButton(
    text='Поделится результатом',
    callback_data='share'
)

start_kb = InlineKeyboardMarkup(
    inline_keyboard=[[start_quiz_btn],
                     [about_btn]])

about_kb = InlineKeyboardMarkup(
    inline_keyboard=[[zoo_url_btn],
                     [start_quiz_btn]])

options_kb = InlineKeyboardMarkup(
    inline_keyboard=[[answer_1_btn, answer_2_btn],
                     [answer_3_btn, answer_4_btn]])

result_kb = InlineKeyboardMarkup(
    inline_keyboard=[[guardianship_url_btn, ask_btn],
                     [feedback_btn, start_quiz_again_btn],
                     [share_btn]])

ask_kb = InlineKeyboardMarkup(
    inline_keyboard=[[feedback_btn],
                     [start_quiz_btn]])

feedback_kb = InlineKeyboardMarkup(
    inline_keyboard=[[ask_btn],
                     [start_quiz_btn]])

cancel_completed_btn = InlineKeyboardMarkup(
    inline_keyboard=[[start_quiz_btn, ask_btn],
                     [feedback_btn]])

cancel_kb = InlineKeyboardMarkup(
    inline_keyboard=[[cancel_btn]])


def get_share_keyboard(result):
    bot_url = f'https://t.me/{BOT_NAME}'
    text = (f'Моё тотемное животное в Московском зоопарке — {result}!\n'
            f'Узнай и ты своё: {bot_url}')
    vk_text = (f'Моё тотемное животное в Московском зоопарке — {result}!\n'
               f'Узнай и ты своё!')
    img = f'{RESULTS[result]['url']}'

    tg_url = (f'https://t.me/share/url?'
              f'url={img}'
              f'&text={text}')

    vk_url = (f'https://vk.com/share.php?'
              f'url={bot_url}'
              f'&title={vk_text}'
              f'&image={img}'
              f'&noparse=true'
              f'&no_vk_links=1'
              )
    wa_url = f'https://wa.me/?text={text}'

    tg_btn = InlineKeyboardButton(
        text='Telegram',
        url=tg_url
    )

    vk_btn = InlineKeyboardButton(
        text='Вконтакте',
        url=vk_url
    )

    wa_btn = InlineKeyboardButton(
        text='Whatsapp',
        url=wa_url
    )

    share_kb = InlineKeyboardMarkup(
        inline_keyboard=[[tg_btn],
                         [vk_btn],
                         [wa_btn]])

    return share_kb
