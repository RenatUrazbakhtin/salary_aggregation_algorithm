import asyncio

from typing import List

import motor.motor_asyncio
from pymongo import MongoClient

from telegram.client.TgClient import TgClient
from telegram.client.dcs import UpdateObj
from utils import check_input_data

client = MongoClient('mongodb://127.0.0.1:27017')
db = client.newdb
salaries = db.salaries


class Worker:
    """
    Класса сущности - обработчик задач
    """

    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        """
        Класс инициализации воркера
        :param token: api_token телеграм
        :param queue: очередь задач
        :param concurrent_workers: количество воркеров
        """

        self.tg_client = TgClient(token)
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    async def handle_update(self, update: UpdateObj):
        """
        Логика отправки сообщений клиенту
        :param update: Объект полученного сообщения(обновления)
        """

        input_message = update.message.text
        output_message = check_input_data(salaries, input_message)
        await self.tg_client.send_message(update.message.chat.id, output_message)

    async def _worker(self):
        """
        Логика выполнения задачи из очереди
        """

        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            finally:
                self.queue.task_done()

    async def start(self):
        """
        Создание задачи для воркера
        """

        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]

    async def stop(self):
        """
        Завершение задачи воркера
        """

        await self.queue.join()
        for task in self._tasks:
            task.cancel()
