import logging
from telegram import Bot
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

import  constants as const
from utility import timer_timeout
from handlers import add_command_handler, add_messgae_handler, lst_games

bot = Bot(token=const.TOKEN)

logger = logging.getLogger(__name__)


def main():
    # Настройка логирования в stdout
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logger.error("Starting bot")

    # Объявление и инициализация объектов бота и диспетчера
    updater = Updater(token=const.TOKEN, use_context=True)

    dp = updater.dispatcher

    # Регистрация хэндлеров
    add_command_handler(dp)
    add_messgae_handler(dp)

    # Запускаем таймер таймаута
    timer_timeout(lst_games, const.TIMEOUT, bot)

    # Запускаем бот
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
