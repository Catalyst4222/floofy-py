import logging
import re
from random import choice
from typing import Optional

from naff import (
    AllowedMentions,
    Client,
    Extension,
    Member,
    Message,
    PrefixedContext,
    listen,
    prefixed_command,
)
from naff.api.events import MessageCreate

from static.actions import actions

MENTION_REGEX = re.compile(r"(<@!?(\d{17,19})>)")


class Fun(Extension):
    @prefixed_command(name="davo", aliases=["david"])
    async def davo_command(self, ctx: PrefixedContext) -> None:
        name = ctx.message.author.display_name
        await ctx.send(
            f"> **{name}** totally, completely denies that they're a furry! >.<"
        )

    @listen()
    async def on_message_create(self, event: MessageCreate) -> None:
        msg = event.message

        # Check if the message starts with the prefix
        prefixed_message = False

        for prefix in self.bot.default_prefix:
            if msg.content.startswith(prefix):
                prefixed_message = True

        if not prefixed_message:
            return

        # Split the message into its parts, so we can work with them
        command, *args = msg.content.split()
        action = command[2:].lower()

        if actions.get(action) is None:
            return

        # Get the user's display name and receivers
        user = msg.author.display_name
        receivers = self._get_receivers(msg, " ".join(args))
        action_emoji = actions[action]["emoji"]

        if receivers is None:
            action_text = actions[action]["self"]

            self_reply = f"> **{user}** {action_text} {action_emoji}"
            await msg.channel.send(self_reply)
            return

        # Format the reply if there are any receivers
        action_reply = choice(actions[action]["with_receivers"])
        formatted_reply = action_reply.format(receivers=receivers)

        # Send the message
        await msg.channel.send(
            f"> **{user}** {formatted_reply} {action_emoji}",
            allowed_mentions=AllowedMentions.none(),
        )

    @staticmethod
    def _get_receivers(msg: Message, content: Optional[str] = None) -> Optional[str]:
        # sourcery skip: assign-if-exp
        if content is None:
            content = msg.content

        if not content:
            if not msg.message_reference:
                return None

            reply = msg.channel.get_message(msg.message_reference.message_id)
            return f"**{reply.author.display_name}**"

        mentions = re.findall(MENTION_REGEX, content)

        if not mentions:
            return content

        mentions: list[Member] = [msg.guild.get_member(int(uid)) for _, uid in mentions]

        mention_string = ""
        length = len(mentions)

        for (idx, mention) in enumerate(mentions):
            mention_name = mention.display_name

            if idx != 0:
                if idx == length - 1:
                    mention_string += " and "
                else:
                    mention_string += ", "

            mention_string += f"**{mention_name}**"

        return mention_string


logging.ERROR


def setup(bot: Client):
    Fun(bot)
