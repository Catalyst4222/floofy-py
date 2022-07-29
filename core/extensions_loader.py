import os

from core.base import FloofyClient


def load_extensions(bot: FloofyClient):
    _ext_walk(bot)


def reload_all_extensions(bot: FloofyClient):
    is_load = False
    _ext_walk(bot, is_load)


def _ext_walk(bot: FloofyClient, is_load: bool = True):
    action_str = "Loading" if is_load else "Reloading"
    bot.logger.info(f"{action_str} all extensions...")

    for root, dirs, files in os.walk("extensions"):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file = file.removesuffix(".py")
                path = os.path.join(root, file)
                python_import_path = path.replace("/", ".").replace("\\", ".")

                bot.logger.debug(f"{action_str} {python_import_path}")

                if is_load:
                    bot.load_extension(python_import_path)
                else:
                    bot.reload_extension(python_import_path)

    bot.logger.info(f"< {len(bot.interactions[0])} > Global Interactions Loaded")
