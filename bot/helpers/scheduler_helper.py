from apscheduler.job import Job
from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from bot import database
from bot.constants.help_alerts import TURN_TITLE
from bot.decorators.on_callback_query import on_callback_query
from bot.decorators.on_typed_message import on_typed_message
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


def check_job_state(job: Job, module_name: str, must_job_run: bool):
    if job is None:
        raise TelegramBotException(module_name + " is not set in this chat")
    if job.next_run_time and not must_job_run:
        raise TelegramBotException(module_name + " module is already on")
    if job.next_run_time is None and must_job_run:
        raise TelegramBotException(module_name + " module is already off")


def register_connection_switchers(client: ScheduledClient, module_name: str):
    __register_connection_switcher(client, module_name, True)
    __register_connection_switcher(client, module_name, False)

    @on_callback_query(client, filters.regex(r"^" + TURN_TITLE))
    async def switch_connection_query(_, message: Message):
        turn_str: str = message.text[len(TURN_TITLE):]
        await switch_connection(client, message, module_name, True if turn_str == "on" else False)


def __register_connection_switcher(client: ScheduledClient, module_name: str, turn_on: bool):
    @on_typed_message(client, filters.command("on" if turn_on else "off" + "_" + module_name))
    async def func(_, message):
        await switch_connection(client, message, module_name, turn_on)


async def switch_connection(client, message, module_name, turn_on):
    on_or_off_str: str = "on" if turn_on else "off"
    job: Job | None = client.scheduler.get_job(client.get_unique_job_id(message.chat.id, module_name))
    check_job_state(job, module_name, must_job_run=not turn_on)
    if turn_on:
        job.resume()
    else:
        job.pause()
    database.update_gmail_module(message.chat.id, module_is_on=turn_on)
    await client.send_success_reply_message(message, module_name + " module is " + on_or_off_str)
