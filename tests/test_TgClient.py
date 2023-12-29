import unittest

from run_bot import token
from telegram.client.TgClient import TgClient


class TestTgClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.token = token
        self.client = TgClient(self.token)

    def test_get_url(self):
        self.assertEqual(self.client.get_url('getUpdates'), f'https://api.telegram.org/bot{self.token}/getUpdates')

    async def test_get_updates(self):
        self.assertEqual(await self.client.get_updates(), {'ok': True, 'result': []})

    async def test_get_me(self):
        self.assertEquals(await self.client.get_me(), {'ok': True,'result':{'id':6959677602,'is_bot':True,'first_name':'aggregation_bot','username':'dip_aggregation_bot','can_join_groups':True,'can_read_all_group_messages':False,'supports_inline_queries':False}})
