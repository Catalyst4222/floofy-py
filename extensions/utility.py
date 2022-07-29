import datetime
from random import choice

from naff import Extension, slash_command, InteractionContext, Embed, cooldown, Buckets, Task, IntervalTrigger, Status, \
    Activity, ActivityType, listen

from core.base import FloofyClient
from static.actions import actions
from static.constants import embed_colors, statuses


class Utility(Extension):
    bot: FloofyClient

    @slash_command(
        name="ping",
        description="UTILITY | Checks the bot's latency to the Discord API"
    )
    async def ping_command(self, ctx: InteractionContext) -> None:
        latency = self.bot.latency * 1000
        avatar_url = self.bot.user.avatar.url

        reply = Embed(
            title="Discord API Latency",
            description=f"What's up, dog? :wolf:\nCurrent latency: `{latency:,.2f}ms`",
            thumbnail=avatar_url,
            timestamp=datetime.datetime.now().astimezone()
        )

        await ctx.send(embed=reply)

    @slash_command(
        name="help",
        description="UTILITY | Returns a list of available commands"
    )
    @cooldown(Buckets.MEMBER, 1, 10)
    async def help_command(self, ctx: InteractionContext) -> None:
        actions_embed = self.get_actions_embed()

        await ctx.send(embed=actions_embed)
        return

    @staticmethod
    def get_actions_embed() -> Embed:
        # Get all the action names available and sort them
        action_names = list(actions.keys())
        action_names.sort()

        # Create the embed object to show the user the actions
        embed: Embed = Embed(
            title="Action commands",
            color=embed_colors["main_color"],
            description=f"The following commands are available as actions:\n```{', '.join(action_names)}```"
        )

        return embed

    @Task.create(IntervalTrigger(minutes=10))
    async def change_status(self):
        new_status = choice(statuses)

        await self.bot.change_presence(
            status=Status.ONLINE,
            activity=Activity(
                name=new_status,
                type=ActivityType.PLAYING
            )
        )

    @listen()
    async def on_ready(self):
        # Start up the change status task
        self.change_status.start()

        # Log to the console that we've started the task
        self.bot.logger.info("Started status change task!")


def setup(bot: FloofyClient):
    Utility(bot)
