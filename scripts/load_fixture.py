import asyncio
import json
import logging
from pathlib import Path

from sqlalchemy import text, select, insert
from sqlalchemy.exc import IntegrityError

from src.model import meta
from src.storage.db import engine, async_session


# NOTE: Не использовать для прода. Нужно использовать alembic
async def load_fixture(files: list[Path]) -> None:
    for file in files:
        with open(f'../{file}', 'r') as f:
            async with async_session() as db:
                table = meta.metadata.tables[file.stem]
                await db.execute(insert(table).values(json.load(f)))
                await db.commit()


if __name__ == '__main__':
    asyncio.run(load_fixture(
        [
            Path('fixtures/public.gift.json'),
        ]
    ))
