import asyncio

import app  # Для работы конфига logging
import logging as log

import database
from bot import start_bot

if __name__ == "__main__":
    try:
        # log.disable(15)
        # log.log(15, 'save')
        start_bot.main()
    except KeyboardInterrupt:
        pass
    finally:
        asyncio.run(database.close_database())






