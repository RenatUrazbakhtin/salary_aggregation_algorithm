from dataclasses import field
from typing import ClassVar, Type, List, Optional

from marshmallow_dataclass import dataclass
from marshmallow import Schema, EXCLUDE

# Получение данных отправителя в виде схемы
@dataclass
class MessageFrom:
    id: int
    first_name: str
    last_name: Optional[str]
    username: str

    class Meta:
        unknown = EXCLUDE

# Получение данных чата в виде схемы
@dataclass
class Chat:
    id: int
    type: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None

    class Meta:
        unknown = EXCLUDE

# Получение данных сообщения отправителя в виде схемы
@dataclass
class Message:
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    text: Optional[str] = None

    class Meta:
        unknown = EXCLUDE

# Получение сообщения от отправителя в виде схемы
@dataclass
class UpdateObj:
    update_id: int
    message: Message

    class Meta:
        unknown = EXCLUDE

# Получение статуса запроса и создание схемы запроса
@dataclass
class GetUpdatesResponse:
    ok: bool
    result: List[UpdateObj]

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE

# Получение объекта отправки сообщения в виде схемы
@dataclass
class SendMessageResponse:
    ok: bool
    result: Message

    Schema: ClassVar[Type[Schema]] = Schema

    class Meta:
        unknown = EXCLUDE