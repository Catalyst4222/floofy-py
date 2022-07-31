import asyncio
import datetime

import naff
from naff import (
    Button,
    Client,
    Context,
    Embed,
    Extension,
    InteractionContext,
    OptionTypes,
    slash_command,
    slash_option,
)

from static.constants import embed_colors
from utils.extensions_loader import reload_all_extensions


class OwnerOnly(Extension):
    def __init__(self, bot: Client):
        self.bot = bot
        self.add_ext_check(self.owner_check)

    @staticmethod
    async def owner_check(ctx: Context):
        return ctx.bot.owner.id == ctx.author.id

    @slash_command(
        name="botstatus", description="OWNER ONLY | Check the status of the bot"
    )
    async def bot_status(self, ctx: InteractionContext):
        now = datetime.datetime.now()
        socket_created = ctx.bot.start_time
        uptime = now - socket_created

        guild_count = len(ctx.bot.guilds)
        guild_text = "server" if guild_count == 1 else "servers"

        latency = ctx.bot.average_latency * 1000

        # Create a new embed object
        status_embed = Embed(
            title="FloofyBot Status",
            description=f"Current status of the bot is: **{ctx.bot.status.value}**",
            color=embed_colors["main_color"],
            timestamp=now,
            thumbnail=ctx.bot.user.avatar.url,
        )

        # Add fields for the status data
        status_embed.add_field(
            name="Servers", value=f"{guild_count} {guild_text}", inline=True
        )
        status_embed.add_field(name="Members", value="Who knows?", inline=True)
        status_embed.add_field(
            name="Startup Time",
            value=f"<t:{int(socket_created.timestamp())}:f>",
            inline=True,
        )
        status_embed.add_field(name="Uptime", value=f"{str(uptime)[:-4]}", inline=True)
        status_embed.add_field(
            name="Avg. Latency", value=f"{latency:,.2f}ms", inline=True
        )
        status_embed.add_field(
            name="Version Info", value=f"naff@{naff.__version__}", inline=True
        )

        await ctx.send(embed=status_embed)

    @slash_command(
        name="generateinvite",
        description="OWNER ONLY | Generate an invite link for the bot",
    )
    @slash_option(
        name="admin_perms",
        description="If the bot should have administration permissions or not",
        opt_type=OptionTypes.BOOLEAN,
        required=False,
    )
    async def generate_invite(self, ctx: InteractionContext, admin_perms: bool = False):
        permissions = "8" if admin_perms else "412317173824"
        embed_perm_string = "administrator" if admin_perms else "normal"
        base_url = "https://discord.com/api/oauth2/authorize"
        client_id = self.bot.app.id
        full_url = f"{base_url}?client_id={client_id}&permissions={permissions}&scope=bot%20applications.commands"

        invite_button = Button(label="Invite", style=5, url=full_url)

        embed = Embed(
            title="Invite me to your server!",
            description=f"Click the button below to invite me to your server with `{embed_perm_string}` permissions.",
            color=embed_colors["main_color"],
        )

        await ctx.send(embed=embed, components=[invite_button])

    @slash_command(name="shutdown", description="OWNER ONLY | Shuts the bot down.")
    async def shutdown(self, ctx: InteractionContext):
        shutdown_timestamp = datetime.datetime.now() + datetime.timedelta(seconds=15)
        shutdown_message = await ctx.send(
            f"**Floofy** is shutting down <t:{int(shutdown_timestamp.timestamp())}:R>"
        )

        await asyncio.sleep(15)
        await shutdown_message.delete()
        await self.bot.stop()

    @slash_command(
        name="reload", description="OWNER ONLY | Reload the bot's extensions"
    )
    @slash_option(
        name="extension_name",
        description="Name of the extension to reload. Leave blank to reload all extensions",
        opt_type=OptionTypes.STRING,
        required=False,
    )
    async def reload(self, ctx: InteractionContext, extension_name: str = "none"):
        if extension_name == "none":
            all_ext_reload_msg = await ctx.send(
                "Reloading all extensions, please hold..."
            )

            reload_all_extensions(self.bot)

            await all_ext_reload_msg.edit("All extensions successfully reloaded!")
            await all_ext_reload_msg.delete(10)
            return

        ext_reload_msg = await ctx.send(
            f"Reloading extension **{extension_name}**, please hold..."
        )
        path_to_reload = f"extensions.{extension_name}"

        try:
            self.bot.reload_extension(path_to_reload)
            ext_reload_str = f"Extension **{extension_name}** successfully reloaded!"
        except ModuleNotFoundError:
            ext_reload_str = f"Extension **{extension_name}** was not found!"

        await ext_reload_msg.edit(ext_reload_str)
        await ext_reload_msg.delete(10)


def setup(bot: Client):
    OwnerOnly(bot)
