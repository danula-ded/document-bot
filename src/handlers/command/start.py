import aio_pika
import msgpack
from aio_pika import ExchangeType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InlineKeyboardMarkup

from config.settings import settings
from src.schema.gift import GiftMessage
from .router import router
from src.handlers.states.auth import AuthGroup
from ..buttons import START_GIFTING
from ...storage.rabbit import channel_pool


@router.message(Command('start'))
async def start_cmd(message: Message, state: FSMContext) -> None:
    await state.set_data({})
    await state.get_data()

    await state.set_state(AuthGroup.authorized)
    await state.get_state()
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange("user_gifts", ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(
            settings.USER_GIFT_QUEUE_TEMPLATE.format(
                user_id=message.from_user.id,
            ),
            durable=True,
        )

        users_queue = await channel.declare_queue(
            'user_messages',
            durable=True,
        )

        # Binding queue
        await queue.bind(
            exchange,
            settings.USER_GIFT_QUEUE_TEMPLATE.format(
                user_id=message.from_user.id,
            ),
        )
        # Binding queue
        await users_queue.bind(
            exchange,
            'user_messages'
        )

        await exchange.publish(
            aio_pika.Message(
                msgpack.packb(
                    GiftMessage(
                        user_id=message.from_user.id,
                        action='get_gifts',
                        event='gift'
                    )
                ),
                # correlation_id=context.get(HeaderKeys.correlation_id)
            )
            ,
            'user_messages'
        )


    # await state.set_data({
    #     'button1': 1,
    #     'button2': 1,
    # })

    # # callback buttons
    # inline_btn_1 = InlineKeyboardButton(text='Первая кнопка!', callback_data='button1')
    # inline_btn_2 = InlineKeyboardButton(text='Вторая кнопка!', callback_data='button2')
    # markup = InlineKeyboardMarkup(
    #     inline_keyboard=[[inline_btn_1, inline_btn_2]]
    # )

    button = KeyboardButton(text=START_GIFTING)
    markup = ReplyKeyboardMarkup(keyboard=[[button]])

    await message.answer('Hello!', reply_markup=markup)
