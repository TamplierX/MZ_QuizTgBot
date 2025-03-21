import logging
from logging.handlers import RotatingFileHandler


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик для уровня DEBUG.
    debug_handler = RotatingFileHandler('logs/debug.log', maxBytes=1024 * 1024 * 5, backupCount=5)
    debug_handler.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                                        '[%(asctime)s] - %(name)s - %(message)s')
    debug_handler.setFormatter(debug_formatter)
    logger.addHandler(debug_handler)

    # Создаем обработчик для уровня INFO.
    info_handler = RotatingFileHandler('logs/info.log', maxBytes=1024 * 1024 * 5, backupCount=5)
    info_handler.setLevel(logging.INFO)
    info_formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                                       '[%(asctime)s] - %(name)s - %(message)s')
    info_handler.setFormatter(info_formatter)
    logger.addHandler(info_handler)

    # Создаем обработчик для уровня WARNING.
    warning_handler = RotatingFileHandler('logs/warning.log', maxBytes=1024*1024*5, backupCount=5)
    warning_handler.setLevel(logging.WARNING)
    warning_formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                                          '[%(asctime)s] - %(name)s - %(message)s')
    warning_handler.setFormatter(warning_formatter)
    logger.addHandler(warning_handler)

    # Создаем обработчик для уровня ERROR.
    error_handler = RotatingFileHandler('logs/error.log', maxBytes=1024*1024*5, backupCount=5)
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                                        '[%(asctime)s] - %(name)s - %(message)s')
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)

    # Создаем обработчик для уровня CRITICAL.
    critical_handler = RotatingFileHandler('logs/critical.log', maxBytes=1024*1024*5, backupCount=5)
    critical_handler.setLevel(logging.CRITICAL)
    critical_formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                                           '[%(asctime)s] - %(name)s - %(message)s')
    critical_handler.setFormatter(critical_formatter)
    logger.addHandler(critical_handler)

    # Добавляем обработчик для вывода в консоль.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                                          '[%(asctime)s] - %(name)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
