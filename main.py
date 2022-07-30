import os
from random import choice

from dotenv import load_dotenv
from naff import Intents, Status
from naff.ext.debug_extension import DebugExtension

from core.logging import init_logging
from core.base import FloofyClient
from core.extensions_loader import load_extensions
from static.constants import statuses

# Load the environmental vars from the .env file
load_dotenv()

# Initialise logging
init_logging()

# Create our bot instance
bot = FloofyClient(
    intents=Intents.ALL,
    auto_defer=True,
    status=Status.ONLINE,
    activity=choice(statuses),
    default_prefix=("f.", "F.", "f!", "F!"),
)

# Load the debug extension if that is wanted
if os.getenv("LOAD_DEBUG_COMMANDS") == "true":
    DebugExtension(bot=bot)

# Load all extensions in the ./extensions folder
load_extensions(bot=bot)

if __name__ == "__main__":
    # Start the bot
    bot.start(os.getenv("DISCORD_TOKEN"))
