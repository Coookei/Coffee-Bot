import logging

from discord.ext import commands

log = logging.getLogger(__name__)


class LoggerCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    class LoggingFilter(logging.Filter):
        def filter(self, record):
            # if record.getMessage().startswith('Shard ID None has sent the RESUME payload.') \
            #         or record.getMessage().startswith('Shard ID None has successfully RESUMED session') \
            #         or record.getMessage().startswith('Shard ID None has sent the IDENTIFY payload.') \
            #         or record.getMessage().startswith('Shard ID None has connected to Gateway: ["') \
            #         or record.getMessage().startswith('logging in using static token') \
            if record.getMessage().startswith('PyNaCl is not installed, voice will NOT be supported'):
                #     # or record.getMessage().startswith('Got a request to RESUME the websocket.') \
                #     # or record.getMessage().startswith('Websocket closed'):
                #
                return False  # dont log it
            return True

    async def cog_load(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%I:%M:%S %p')

        logging.getLogger('discord.gateway').addFilter(self.LoggingFilter())
        logging.getLogger('discord.client').addFilter(self.LoggingFilter())
        logging.getLogger('aiohttp.access').setLevel("WARNING")

    async def cog_unload(self) -> None:
        self.reset_logging()

    def reset_logging(self):
        manager = logging.root.manager
        manager.disabled = logging.NOTSET
        for logger in manager.loggerDict.values():
            if isinstance(logger, logging.Logger):
                logger.setLevel(logging.NOTSET)
                logger.propagate = True
                logger.disabled = False
                logger.filters.clear()
                handlers = logger.handlers.copy()
                for handler in handlers:
                    # Copied from `logging.shutdown`.
                    try:
                        handler.acquire()
                        handler.flush()
                        handler.close()
                    except (OSError, ValueError):
                        pass
                    finally:
                        handler.release()
                    logger.removeHandler(handler)


async def setup(bot):
    await bot.add_cog(LoggerCog(bot))
