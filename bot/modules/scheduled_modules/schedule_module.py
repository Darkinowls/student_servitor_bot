import json
from abc import ABC

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot import database
from bot.database import get_schedule_by_chat_id
from bot.database.models.lesson import Lesson
from bot.decorators.on_typed_message import on_typed_message
from bot.exceptions.telegram_bot_exception import TelegramBotException
from bot.helpers.job_helper import check_job_state
from bot.helpers.json_helper import check_document_is_json, load_schedule_json_from_file
from bot.helpers.schedule_helper import get_lessons_from_schedule_json, get_current_week_number, get_current_time_str, \
    get_current_day_str
from bot.helpers.tmp_helper import create_tmp_json_filepath, create_tmp_json_file
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class ScheduleClient(ScheduledClient):
    _scheduler: AsyncIOScheduler
    _module_name: str

    def _send_on_schedule(self, *args: int | list[Lesson]):
        chat_id = args[0]
        lessons: list[Lesson] = args[1]
        week_num: int = get_current_week_number()
        day_str: str = get_current_day_str()
        time_str: str = get_current_time_str()
        for lesson in lessons:
            if lesson.week == week_num and lesson.day == day_str and lesson.time == time_str:
                self.send_message(chat_id=chat_id, text=lesson.name + '\n' + lesson.link)

    def _add_previous_sessions_to_scheduler(self) -> AsyncIOScheduler:
        for session in database.get_all_schedule_sessions():
            chat_id = int(session.get('chat_id'))
            module_is_on = bool(session.get('module_is_on'))
            lessons: list[Lesson] = get_lessons_from_schedule_json(
                session.get('schedule'))  # it checks and gets lessons
            job: Job = self._add_job(chat_id, 60, lessons)
            if not module_is_on:
                job.pause()
        return self._scheduler

    def __init__(self, bot_name, api_id, api_hash, bot_token):
        self._module_name = "schedule"
        super().__init__(bot_name, api_id, api_hash, bot_token)

        @on_typed_message(self, filters.command("schedule"))
        async def set_gmail_connection(_, message: Message):
            check_document_is_json(message.document)
            filepath: str = await self.download_media(message,
                                                      file_name=create_tmp_json_filepath("schedule", message.chat.id))
            schedule: list[dict] = load_schedule_json_from_file(filepath)
            lessons: list[Lesson] = get_lessons_from_schedule_json(schedule)  # it checks and gets lessons
            database.upsert_schedule(chat_id=message.chat.id, schedule=schedule)
            self._add_job(message.chat.id, 60, lessons)
            await self.send_reply_message(message, "Schedule module is successfully set!")

        @on_typed_message(self, filters.command("my_schedule"))
        async def send_schedule_file(_, message: Message):
            schedule = get_schedule_by_chat_id(message.chat.id)
            if schedule is None:
                await self.send_reply_document(message, "schedule.example.json")
                raise TelegramBotException("You have not set a schedule yet. Here is an example above.")
            filepath: str = create_tmp_json_file("my_schedule", message.chat.id, json.dumps(schedule))
            await self.send_reply_document(message, filepath)