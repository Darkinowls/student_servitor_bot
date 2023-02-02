import json
from pyrogram.types import Document

from bot.constants.database import SCHEDULE
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.database.lesson import Lesson


def check_document_is_json(document: Document) -> bool:
    if document is None or not document.file_name.endswith(".json"):
        raise TelegramBotError("Json document is required")
    return True


def load_schedule_json_from_file(filepath) -> list[dict]:
    try:
        with open(filepath) as f:
            return json.load(f).get(SCHEDULE)
    except ValueError:
        raise TelegramBotError('JSON syntax error')
    except KeyError:
        raise TelegramBotError('No field "schedule" in the json')


def get_lessons_from_schedule_json(schedule: list[dict]) -> list[Lesson]:
    return [Lesson(lesson_json) for lesson_json in schedule]
