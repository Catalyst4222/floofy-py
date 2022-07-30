import logging
import os

from naff import Client, listen, logger_name


class FloofyClient(Client):
    """Subclass of naff.Client with our own logger and on_startup event"""

    logger = logging.getLogger(logger_name)

    @listen()
    async def on_startup(self):
        """Gets triggered on startup"""

        self.logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
        await self.synchronise_interactions(delete_commands=True)
