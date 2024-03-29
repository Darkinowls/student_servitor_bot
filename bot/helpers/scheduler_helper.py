import numpy as np
from apscheduler.job import Job
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.constants.database import SCHEDULE
from bot.constants.emoji import PLAY_EMOJI, PAUSE_EMOJI
from bot.constants.general import WHITESPACE, UNDERLINE
from bot.constants.gmail import GMAIL
from bot.database.session import Session
from bot.decorators.on_callback_query import on_callback_query
from bot.decorators.on_message import on_message
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


def check_job_state(job: Job, module_name: str, must_job_run: bool):
    if job is None:
        raise TelegramBotError("модуль" + WHITESPACE + translate_module_name_into_ukrainian(
            module_name) + WHITESPACE + "не встановлений у цьому чаті")
    if job.next_run_time and not must_job_run:
        raise TelegramBotError(
            "модуль" + WHITESPACE + translate_module_name_into_ukrainian(module_name) + WHITESPACE + "вже увімкнений")
    if job.next_run_time is None and must_job_run:
        raise TelegramBotError(
            "модуль" + WHITESPACE + translate_module_name_into_ukrainian(module_name) + WHITESPACE + "уже вимкнений")


def register_connection_switchers(client: ScheduledClient, module_name: str, session: Session):
    __register_connection_switcher(client, module_name, True, session)
    __register_connection_switcher(client, module_name, False, session)

    @on_callback_query(client, filters.regex(r"^" + module_name))
    async def switch_connection_query(_, message: Message):
        turn_str: str = message.text.split(UNDERLINE, 1)[1]
        await switch_connection(client, message, module_name, get_turn_bool(turn_str), session)
        await message.edit_reply_markup(create_keyboard_markup(module_name, reverse_turn_str(turn_str)))


def __register_connection_switcher(client: ScheduledClient, module_name: str, turn_bool: bool, session: Session):
    @on_message(client, filters.command(get_turn_str(turn_bool) + "_" + module_name))
    async def func(_, message):
        await switch_connection(client, message, module_name, turn_bool, session)


async def switch_connection(client: ScheduledClient, message, module_name, turn_bool, session: Session):
    job: Job | None = client.scheduler.get_job(client.get_unique_job_id(message.chat.id, module_name))
    check_job_state(job, module_name, must_job_run=not turn_bool)
    session.set_session_module_is_on(message.chat.id, module_is_on=turn_bool)
    if turn_bool:
        job.resume()
        await client.send_reply_message(message, PLAY_EMOJI + WHITESPACE +
                                        "модуль" + WHITESPACE +
                                        translate_module_name_into_ukrainian(module_name)
                                        + WHITESPACE + "увімкнений")
    else:
        job.pause()
        await client.send_reply_message(message, PAUSE_EMOJI + WHITESPACE +
                                        "модуль" + WHITESPACE +
                                        translate_module_name_into_ukrainian(module_name)
                                        + " вимкнений")


def create_keyboard_markup(module_name: str, turn_str: str):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(translate_turn_str_into_ukrainian(turn_str)
                                     + WHITESPACE + "модуль" + WHITESPACE +
                                     translate_module_name_into_ukrainian(module_name),
                                     callback_data=module_name + UNDERLINE + turn_str),
            ]
        ]
    )


def reverse_turn_str(turn_str) -> str:
    return "on" if turn_str == "off" else "off"


def get_turn_str(turn_on: bool) -> str:
    return "on" if turn_on else "off"


def get_turn_bool(turn_str: str) -> bool:
    return True if turn_str == "on" else False


def translate_turn_str_into_ukrainian(turn_str: str) -> str:
    return 'увімкнути' if turn_str == "on" else 'вимкнути'


def translate_module_name_into_ukrainian(module_name: str) -> str:
    return "розкладів" if module_name == SCHEDULE else module_name


def make_keyboard_list(texts: list[str]) -> list:
    for i in range(3, 0, -1):
        if len(texts) % i == 0:
            unique_faculties_list = np.array(texts).reshape((-1, i))
            return unique_faculties_list
    return []
