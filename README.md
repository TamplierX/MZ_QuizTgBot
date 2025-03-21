# Телеграм-бот-викторина для популяризации программы опеки Московского зоопарка.

## Структура проекта
```plaintext
MZ_QuizTgBot/
├── config_data/             # Папка для конфигураций.
│   ├── config.py            # Конфигурация бота.
│   └── config_logging.py    # Конфигурация logging.
├── database/                # Папка для настроек БД.
│   └── database.py          # Настройка и управление БД.
├── handlers/                # Обработчики команд и сообщений от пользователя
│   ├── other_handlers.py    # Обработчиком любых сообщений пользователя, которые не попали в другие обработчики.
│   └── user_handlers.py     # Основные обработчики апдейтов.
├── keyboards/               # Папка с клавиатурами бота.
│   ├── kb_utils.py          # Клавиатуры для работы с пользователями.
│   └── set_menu.py          # Модуль для формирования главного меню бота.
├── lexicon/                 # Папка для хранения словарей бота.
│   └── lexicon_ru.py        # Файл со словарем соответствий команд и запросов отображаемым текстам.
├── logs/                    # Папка для хранения логов.
├── media/                   # Папка для хранения медиа файлов.
├── services/                # Папка с биснес логикой бота.
│   ├── logic.py             # Вспомогательные функции для реализации логики.
│   ├── questions.py         # Список с вопросами, вариантами ответов для них, балами для определения результата.
│   ├── results.py           # Список с сылками на изображения животных.
│   └── variables.py         # Статические переменные.
├── states/                  # Папка для состояний.
│   └──states.py             # Файл для оглагения состояний.
├── main.py                  # Точка входа в бот.
├── .env                     # Файл с переменными окружения для конфигурации бота.
├── .env.example             # Файл с примерами секретов для GitHub.
├── .gitignore               # Файл, сообщающий гиту какие файлы и директории не отслеживать.
├── requirements.txt         # Зависимости для Python.
└── README.md                # Описание
```
## Требования

- Python 3.12
- Aiogram 3.17
- Redis 3.0.504 - локальный сервер.

## Установка и запуск

1. Создайте файл .env в корне проекта и запишите в него токен бота (пример в файле .env.example).

2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3. Установите зависимости:
   ```bash
    pip install -r requirements.txt
    ```
   
4. Запустите локальный сервер Redis ("redis-server.exe").

5. Запустите бота:
    ```bash
    py main.py
    ```

## Функциональные возможности

- Есть модуль для проведения викторины.
- Можно задать вопрос сотруднику зоопарка.
- Можно оставить обратную связь о боте.
- Можно поделиться результатом последней пройденной викторины. 


## Дополнительные настройки бота

В файле services/variables.py можно настроить:
- Количество вопросов в викторине.
- Указать ID сотрудника зоопарка в Telegram, что б он получал уведомления о вопросах и отзывах пользователей.
- Указать имя бота для репоста в соцсетях.


