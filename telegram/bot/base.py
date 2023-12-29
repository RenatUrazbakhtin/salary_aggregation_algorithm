import asyncio

from telegram.bot.poller import Poller
from telegram.bot.worker import Worker


class Bot:
    """
    Класс сущности - Бот
    """

    def __init__(self, token: str, n: int):
        """
        Инициализация класса с очередью задач, пула задач, воркера задач
        :param token: api_token телеграм бота
        :param n: количество воркеров
        """

        self.queue = asyncio.Queue()
        self.poller = Poller(token, self.queue)
        self.worker = Worker(token, self.queue, n)

    async def start(self):
        """
        Функция старта бота(пула и воркеров)
        """

        await self.poller.start()
        await self.worker.start()

    async def stop(self):
        """
        Фукнция остановки бота(пула и воркеров)
        """

        await self.poller.stop()
        await self.worker.stop()