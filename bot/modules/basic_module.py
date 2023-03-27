from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message

from bot.constants.commands import JSON, HI, COPY, WEEK, W, START, HELP
from bot.constants.help_alerts import ALL_COMMANDS
from bot.decorators.on_message import on_message
from bot.decorators.on_typed_message import on_typed_message
from bot.helpers.json_helper import get_tmp_json_file
from bot.helpers.parameter_helper import get_single_text_parameter
from bot.helpers.datetime_helper import get_current_week_number_formatted
from bot.modules.simple_client import SimpleClient


class BasicModule(SimpleClient):

    def __init__(self, api_id, api_hash, bot_token):
        super().__init__(api_id=api_id, api_hash=api_hash, bot_token=bot_token)

        @on_message(self, filters.command(JSON))
        async def get_json_from_message(_, message: Message):
            """
            To get json from the message has sent
            """
            print(message)
            filepath: str = get_tmp_json_file(filename="message",
                                              chat_id=message.chat.id,
                                              data=message.__dict__)
            await self.send_document(chat_id=message.chat.id, document=filepath)

        @on_message(self, filters.command(HI))
        async def say_hello(_, message: Message):
            """
            Everyone can say hello to Bot!
            """
            await self.send_reply_message(message, (await self.get_me()).first_name + " welcomes you!")

        @on_typed_message(self, filters.reply & filters.command(COPY))
        async def set_message_text(_, message: Message):
            await self.edit_replied_message(message, text=get_single_text_parameter(message.text))

        @on_typed_message(self, filters.command(COPY))
        async def copy_message_text(_, message: Message):
            await self.send_reply_message(message, text=get_single_text_parameter(message.text))

        @on_typed_message(self, filters.command([WEEK, W]))
        async def print_week_number(_, message: Message):
            await self.send_reply_message(message,
                                          text=f"Today is the {get_current_week_number_formatted()} week")

        @on_typed_message(self, filters.command([START, HELP]))
        async def send_help_message(_, message: Message):
            await message.reply_text(ALL_COMMANDS, parse_mode=ParseMode.HTML)
