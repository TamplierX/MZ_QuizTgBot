import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from database.database import db_start
from config_data.config import Config, load_config
from config_data.config_logging import setup_logging
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, user_handlers


logger = logging.getLogger(__name__)

# Загружаем конфиг бота.
config: Config = load_config()

# Создаем экземпляр бота.
bot = Bot(
    token=config.tg_bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


# Функция конфигурирования и запуска бота
async def main() -> None:
    # Конфигурируем логирование.
    setup_logging()

    # Подключаем Redis.
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    # Создаем или проверяем базу данных.
    await db_start()

    # Настраиваем главное меню бота.
    await set_main_menu(bot)

    # Регистрируем роутеры в диспетчере.
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
