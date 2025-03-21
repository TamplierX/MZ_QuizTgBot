from aiogram import F, Router
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command, CommandStart, StateFilter
import logging

from lexicon.lexicon_ru import LEXICON_RU
from keyboards.kb_utils import (start_kb, about_kb, options_kb, result_kb, cancel_kb, get_share_keyboard,
                                ask_kb, feedback_kb, cancel_completed_btn)
from states.states import FSMQuiz, FSMAsk, FSMFeedback
from database.database import add_user_db, upd_user_db, add_ask_db, add_feedback_db, get_user_info
from services.results import RESULTS
from services.variables import QUESTS_COUNT, SUPPORT_USER
from main import bot
from services.logic import (get_random_quests, get_quest, get_quest_text, get_quest_options,
                            set_quest_scores, quiz_result, get_msc_date)


router = Router()
logger = logging.getLogger(__name__)

# Обработчик команды /start когда есть активный state.
@router.message(CommandStart(), ~StateFilter(default_state))
async def process_error_command(message: Message):
    await message.answer(text=LEXICON_RU['error'], reply_markup=cancel_kb)

# Обработчик команды /start.
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    try:
        photo = FSInputFile(f'media/pictures/MZoo_logo.jpg')
        await add_user_db(message.from_user.id, message.from_user.username)
        await message.answer_photo(photo=photo, caption=LEXICON_RU['/start'], reply_markup=start_kb)
    except Exception as e:
        logger.error(f"Error from User {message.from_user.id} in /start command handler: {e}")
        await message.reply(LEXICON_RU['except_error'])

# Обработчик команды /help.
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

# Обработчик кнопки "Узнать больше".
@router.callback_query(F.data == 'about')
async def process_about_command(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['about'], reply_markup=about_kb)
    await callback.answer()

# Обработчик кнопки "Отмена" когда есть активный state.
@router.callback_query(F.data == 'cancel', ~StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery, state: FSMContext):
    # await callback.message.edit_text(text=callback.message.text, reply_markup=None)
    await callback.message.answer(text=LEXICON_RU['/cancel'], reply_markup=cancel_completed_btn)
    await state.clear()
    await callback.answer()

# Обработчик команды /cancel когда есть активный state.
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/cancel'], reply_markup=cancel_completed_btn)
    await state.clear()

# Обработчик команды /cancel когда нет активного state.
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(text=LEXICON_RU['error_cancel'], reply_markup=cancel_completed_btn)

# Обработчик кнопки "Отмена" когда нет активного state.
@router.callback_query(F.data == 'cancel', StateFilter(default_state))
async def process_cancel_command(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['error_cancel'], reply_markup=cancel_completed_btn)
    await callback.answer()

# Обработчик кнопки "Задать вопрос" когда есть активный state.
@router.callback_query(F.data == 'ask', ~StateFilter(default_state))
async def process_ask_error(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['error'], reply_markup=cancel_kb)
    await callback.answer()

# Обработчик кнопки "Задать вопрос" когда нет активного state.
@router.callback_query(F.data == 'ask', StateFilter(default_state))
async def process_ask(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['ask'])
    await state.set_state(FSMAsk.ask_state)
    await callback.answer()

# Обработчик сообщения пользователя когда активный state для вопросов.
@router.message(StateFilter(FSMAsk.ask_state))
async def process_ask_sent(message: Message, state: FSMContext):
    try:
        await add_ask_db(get_msc_date(message.date), message.from_user.id, message.text)
        user = await get_user_info(message.from_user.id)

        if message.from_user.username:
            username = f'username: @{message.from_user.username}, \n'
        else:
            username = '\n'
        # Отправляем вопрос от пользователя сотруднику зоопарка.
        await bot.send_message(SUPPORT_USER, text=f'❓ <b>Получен вопрос:</b> ❓\n'
                                                  f'{get_msc_date(message.date)}\n'
                                                  f'Пользователь бота: '
                                                  f'<a href="tg://user?id={message.from_user.id}">User ID</a>, '
                                                  f'{username}'
                                                  f'Количество пройденных викторин: {user[3]}, \n'
                                                  f'Последний результат викторины: {user[4]}. \n\n'
                                                  f'<b>Вопрос:</b> {message.text}')
        await state.clear()
        await message.answer(text=LEXICON_RU['ask_answer'], reply_markup=ask_kb)
    except Exception as e:
        logger.error(f"Error from User {message.from_user.id} in ask_send callback handler: {e}")
        await message.answer(LEXICON_RU['except_error'])

# Обработчик кнопки "Оставить отзыв" когда есть активный state.
@router.callback_query(F.data == 'feedback', ~StateFilter(default_state))
async def process_feedback_error(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['error'],
                                  reply_markup=cancel_kb)
    await callback.answer()

# Обработчик кнопки "Оставить отзыв" когда нет активного state.
@router.callback_query(F.data == 'feedback', StateFilter(default_state))
async def process_feedback(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU['feedback'])
    await state.set_state(FSMFeedback.feedback_state)
    await callback.answer()

# Обработчик сообщения пользователя когда активный state для обратной связи.
@router.message(StateFilter(FSMFeedback.feedback_state))
async def process_ask_sent(message: Message, state: FSMContext):
    try:
        await add_feedback_db(get_msc_date(message.date), message.from_user.id, message.text)
        user = await get_user_info(message.from_user.id)

        if message.from_user.username:
            username = f'username: @{message.from_user.username}, \n'
        else:
            username = '\n'
        # Отправляем обратную связь от пользователя сотруднику зоопарка.
        await bot.send_message(SUPPORT_USER, text=f'⚙️ <b>Получен отзыв:</b> ⚙️\n'
                                                  f'{get_msc_date(message.date)}\n'
                                                  f'Пользователь бота: '
                                                  f'<a href="tg://user?id={message.from_user.id}">User ID</a>, '
                                                  f'{username}'
                                                  f'Количество пройденных викторин: {user[3]}, \n'
                                                  f'Последний результат викторины: {user[4]}. \n\n'
                                                  f'<b>Отзыв:</b> {message.text}')
        await state.clear()
        await message.answer(text=LEXICON_RU['feedback_answer'], reply_markup=feedback_kb)
    except Exception as e:
        logger.error(f"Error from User {message.from_user.id} in feedback_send callback handler: {e}")
        await message.answer(LEXICON_RU['except_error'])

# Обработчик кнопки "Оставить отзыв" когда есть активный state.
@router.callback_query(F.data == 'share', ~StateFilter(default_state))
async def process_share_error(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['error'], reply_markup=cancel_kb)
    await callback.answer()

# Обработчик кнопки "Оставить отзыв" когда нет активного state.
@router.callback_query(F.data == 'share', StateFilter(default_state))
async def process_share(callback: CallbackQuery):
    try:
        user = await get_user_info(callback.from_user.id)
        await callback.message.answer(text=LEXICON_RU['share'], reply_markup=get_share_keyboard(user[4]))
    except Exception as e:
        logger.error(f"Error from User {callback.from_user.id} in share callback handler: {e}")
        await callback.answer(LEXICON_RU['except_error'])
    finally:
        await callback.answer()

# Обработчик команды /start_quiz когда есть активный state.
@router.message(Command(commands='start_quiz'), ~StateFilter(default_state))
async def process_error_start_quiz(message: Message):
    await message.answer(text=LEXICON_RU['error'], reply_markup=cancel_kb)

# Обработчик кнопки "Начать викторину" когда есть активный state.
@router.callback_query(F.data == 'start_quiz', ~StateFilter(default_state))
async def process_error_start_quiz(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON_RU['error'], reply_markup=cancel_kb)
    await callback.answer()

# Обработчик команды /start_quiz когда нет активного state.
@router.message(Command(commands='start_quiz'), StateFilter(default_state))
async def process_start_quiz(message: Message, state: FSMContext):
    try:
        # Задаем стартовый state data.
        data = await state.get_data()
        data['questions'] = get_random_quests()
        data['current_quest_count'] = 0
        data['current_quest'] = get_quest(data['questions'], data['current_quest_count'])
        data['results'] = {}
        await state.update_data(data)
        await state.set_state(FSMQuiz.quiz_state)
        # Оглашаем о старте викторины и формируем первый вопрос.
        await message.answer(text=f'{LEXICON_RU['start_quiz']}\n\n'
                                  f'❓ <b>Вопрос №{data['current_quest_count'] + 1}:</b> '
                                  f'<i>{get_quest_text(data['current_quest'])}</i> \n\n'
                                  f'{get_quest_options(data['current_quest'])}',
                             reply_markup=options_kb)
    except Exception as e:
        logger.error(f"Error from User {message.from_user.id} in start_quiz command handler: {e}")
        await message.reply(LEXICON_RU['except_error'])

# Обработчик кнопки "Начать викторину" когда нет активного state.
@router.callback_query(F.data == 'start_quiz', StateFilter(default_state))
async def process_start_quiz(callback: CallbackQuery, state: FSMContext):
    try:
        # Задаем стартовый state data.
        data = await state.get_data()
        data['questions'] = get_random_quests()
        data['current_quest_count'] = 0
        data['current_quest'] = get_quest(data['questions'], data['current_quest_count'])
        data['results'] = {}
        await state.update_data(data)
        await state.set_state(FSMQuiz.quiz_state)
        # Оглашаем о старте викторины и формируем первый вопрос.
        await callback.message.answer(text=f'{LEXICON_RU['start_quiz']}\n\n'
                                           f'❓ <b>Вопрос №{data['current_quest_count'] + 1}:</b> '
                                           f'<i>{get_quest_text(data['current_quest'])}</i> \n\n'
                                           f'{get_quest_options(data['current_quest'])}',
                                      reply_markup=options_kb)

    except Exception as e:
        logger.error(f"Error from User {callback.from_user.id} in start_quiz callback handler: {e}")
        await callback.answer(LEXICON_RU['except_error'])
    finally:
        await callback.answer()

# Обрабатываем ответы на вопросы кнопок когда активный state викторины.
@router.callback_query(StateFilter(FSMQuiz.quiz_state))
async def process_answer_send(callback: CallbackQuery, state: FSMContext):
    try:
        # Удаляем кнопки из предыдущего вопроса и редактируем текст.
        await callback.message.edit_text(
            text=f'{callback.message.text}\n\n'
                 f'✅ <b>Ваш ответ: {callback.data}</b>',
            reply_markup=None)
    except Exception as e:
        logger.error(f"Error from User {callback.from_user.id} in answer_send / edit_text callback handler: {e}")

    try:
        # Записываем ответы в state data и формируем следующий вопрос.
        data = await state.get_data()
        set_quest_scores(data['results'], data['current_quest'], callback.data)
        data['current_quest_count'] += 1
        if data['current_quest_count'] < QUESTS_COUNT:
            data['current_quest'] = get_quest(data['questions'], data['current_quest_count'])
        await state.update_data(data)
        if data['current_quest_count'] < QUESTS_COUNT:
            await callback.message.answer(text=f'❓ <b>Вопрос №{data['current_quest_count'] + 1}:</b> '
                                               f'<i>{get_quest_text(data['current_quest'])}</i> \n\n'
                                               f'{get_quest_options(data['current_quest'])}',
                                          reply_markup=options_kb)

        else:
            try:
                # Если было задано нужное количество вопросов - формируем результаты викторины.
                await add_user_db(callback.from_user.id, callback.from_user.username)
                result = quiz_result(data['results'])
                await upd_user_db(callback.from_user.id, result)
                photo = FSInputFile(f'media/pictures/{RESULTS[result]['image']}')
                await callback.message.answer_photo(photo=photo,
                                                    caption=f'🎉Поздравляем тебя с прохождением викторины!🎉\n\n'
                                                            f'{RESULTS[result]["text"]}\n\n'
                                                            f'{LEXICON_RU['result']}',
                                                    reply_markup=result_kb)
                await state.clear()
            except Exception as e:
                logger.error(f"Error from User {callback.from_user.id} in answer_send / result callback handler: {e}")
                await callback.answer(LEXICON_RU['except_error'])

    except Exception as e:
        logger.error(f"Error from User {callback.from_user.id} in answer_send / next_question callback] handler: {e}")
        await callback.answer(LEXICON_RU['except_error'])
    finally:
        await callback.answer()


