import os
from random import choice

from dotenv import load_dotenv
from naff import Client as FloofyClient
from naff import Intents, Status, listen
from naff.ext.debug_extension import DebugExtension

# from core.logging import init_logging
import utils.logger
from static.constants import statuses
from utils.extensions_loader import load_extensions

# Load the environmental vars from the .env file
load_dotenv()

# Initialise logging
logger = utils.logger.get_base_logger("floofy")

# Create our bot instance
floofy_bot = FloofyClient(
    intents=Intents.ALL,
    auto_defer=True,
    status=Status.ONLINE,
    activity=choice(statuses),
    default_prefix=("f.", "F.", "f!", "F!"),
    sync_interactions=False,  # Gets synced during startup
)


@listen()
async def on_startup():
    logger.info(f"{os.getenv('PROJECT_NAME')} - Startup Finished!")
    await floofy_bot.synchronise_interactions(delete_commands=True)


# Load the debug extension if that is wanted
if os.getenv("LOAD_DEBUG_COMMANDS") == "true":
    DebugExtension(bot=floofy_bot)

# Load all extensions in the ./extensions folder
load_extensions(bot=floofy_bot)

if __name__ == "__main__":
    # Start the bot
    floofy_bot.start(os.getenv("DISCORD_TOKEN"))
