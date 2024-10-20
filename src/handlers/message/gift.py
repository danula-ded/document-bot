import asyncio
import json

import aiohttp
import msgpack
from aio_pika import Queue
from aio_pika.exceptions import QueueEmpty
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputFile, BufferedInputFile
from aiogram import F

from config.settings import settings
from ..buttons import START_GIFTING


from .router import router
from ..states.gift import GiftGroup
from ...storage.rabbit import channel_pool
from ...templates.env import render


# @router.message(GiftGroup.gifting)
# async def gifting(message: Message, state: FSMContext) -> None:
#     await message.answer('ypa')


@router.message(F.text == START_GIFTING)
async def start_gifting(message: Message, state: FSMContext) -> None:
    await message.answer('ypa')
    await state.set_state(GiftGroup.gifting)

    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        queue: Queue = await channel.declare_queue(
            settings.USER_GIFT_QUEUE_TEMPLATE.format(user_id=message.from_user.id),
            durable=True,
        )

        # 'name': gift.name,
        # 'photo': gift.photo,
        # 'category': gift.category,

        retries = 3
        for _ in range(retries):
            try:
                gift = await queue.get()
                parsed_gift = msgpack.unpackb(gift.body)

                # async with aiohttp.ClientSession() as session:
                #     async with session.get('https://cdn.velostrana.ru/upload/models/velo/63352/full.jpg') as response:
                #         content = await response.read()
                #
                # photo = BufferedInputFile(content, 'test')

                await message.answer_photo(
                    photo=parsed_gift['photo'],
                    caption=render('gift/gift.jinja2', gift=parsed_gift),
                )
                return
            except QueueEmpty:
                await asyncio.sleep(1)

        await message.answer('Нет подарков')
