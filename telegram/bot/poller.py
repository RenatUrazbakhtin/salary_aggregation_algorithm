import asyncio
from asyncio import Task
from typing import Optional

from telegram.client.TgClient import TgClient




class Poller:
    """
    Класс сущности - пул задач
    """

    def __init__(self, token: str, queue: asyncio.Queue):
        """
        Инициализация пула
        :param token: api_token телеграм
        :param queue: очередь задач
        """

        self.tg_client = TgClient(token)
        self.queue = queue
        self._task: Optional[Task] = None

    async def _worker(self):
        """
        Функция добавления задачи(полученния сообщения) в пул задач
        """

        offset = 0
        while True:
            res = await self.tg_client.get_updates_in_objects(offset=offset, timeout=60)
            for u in res.result:
                offset = u.update_id + 1
                self.queue.put_nowait(u)

    async def start(self):
        """
        Создание задачи для воркера
        """

        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        """
        Остановка задачи
        """

        self._task.cancel()