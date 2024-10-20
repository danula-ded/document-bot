from .base import BaseMessage

# class BaseMessage(TypedDict):
#     event: str

class GiftMessage(BaseMessage):
    action: str
    user_id: int
