import asyncio
import os

import motor.motor_asyncio
from dotenv import load_dotenv

from telegram.bot.base import Bot
from telegram.bot.worker import salaries
from utils import get_data_for_db, get_aggregated_data

load_dotenv()
token = os.getenv('API_TOKEN')

def run():
    """
    Запуск телеграм бота
    """

    salaries.delete_many({})
    salaries.insert_many(get_data_for_db())

    loop = asyncio.get_event_loop()

    bot = Bot(token, 2)
    try:
        print('bot has been started')
        loop.create_task(bot.start())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.stop())
        print('bot has been stopped')


if __name__ == '__main__':
    run()