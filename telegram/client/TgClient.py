from typing import Optional

import aiohttp

from telegram.client.dcs import GetUpdatesResponse, SendMessageResponse



class TgClient:
    """
    Класс сущности - телеграм клиент
    """

    def __init__(self, token: str = ''):
        """
        Инициализация класса по телеграм токену
        :param token: api_token телеграм
        """

        self.token = token

    def get_url(self, method: str):
        """
        Получение ссылки для методов
        :param method: тип запроса
        :return: ссылка для методов
        """

        return f"https://api.telegram.org/bot{self.token}/{method}"

    async def get_me(self) -> dict:
        """
        Получает данные бота
        :return: данные бота в словаре
        """

        url = self.get_url("getMe")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        """
        Получение последних сообщений бота
        :param offset: параметр для получения только новых сообщений
        :param timeout: время ожидания
        :return: последние сообщения в формате json
        """

        url = self.get_url("getUpdates")
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await resp.json()

    async def get_updates_in_objects(self, offset: Optional[int] = None, timeout: int = 0) -> GetUpdatesResponse:
        """
        Получение последнего сообщения в виде экземпляра класса
        :param offset: параметр для получения только новых сообщений
        :param timeout: время ожидания
        :return: последнее сообщение в виде экземляра класса
        """

        res_dict = await self.get_updates(offset=offset, timeout=timeout)
        return GetUpdatesResponse.Schema().load(res_dict)

    async def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """
        Отправка ботом сообщения
        :param chat_id: id чата с клиентом
        :param text: текст сообщения
        :return: отправленное сообщение в виде экземляра класса
        """

        url = self.get_url("sendMessage")
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_dict = await resp.json()
                return SendMessageResponse.Schema().load(res_dict)