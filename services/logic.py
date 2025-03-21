import logging
import random
import pytz

from services.questions import QUESTIONS
from services.variables import QUESTS_COUNT


logger = logging.getLogger(__name__)

# Получаем список случайных вопросов.
def get_random_quests() -> list:
    return random.sample(QUESTIONS, QUESTS_COUNT)

# Получаем вопрос из списка.
def get_quest(quests_list, count):
    return quests_list[count]

# Получаем текст вопроса.
def get_quest_text(quest) -> str:
    return quest['text']

# Получаем варианты ответов на вопрос.
def get_quest_options(quest) -> str:
    try:
        option_str = ''
        marker = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
        options_count = 0
        for option in quest['options']:
            option_str += f'{marker[options_count]}  {option} \n'
            options_count += 1
        return option_str
    except Exception as e:
        logger.error(f"Error in func get_quest_options : {e}")

# Добавляем баллы с ответа в хранилище для результатов.
def set_quest_scores(results, quest, value) -> None:
    try:
        quest_score = quest['scores'][value]

        for item in quest_score:
            for key, value in item.items():
                if key in results:
                    results[key] += value
                else:
                    results[key] = value
    except Exception as e:
        logger.error(f"Error in func set_quest_scores : {e}")

# Получаем итоговый результат викторины.
def quiz_result(results) -> str:
    return max(results, key=results.get)

# Форматируем дату и время по Мск.
def get_msc_date(utc_time):
    try:
        moscow_tz = pytz.timezone('Europe/Moscow')
        moscow_time = utc_time.astimezone(moscow_tz)
        return moscow_time
    except Exception as e:
        logger.error(f"Error in func get_msc_date : {e}")
