from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram.types import Message, InlineKeyboardMarkup

from bot.constants.emoji import CHECK_BOX_EMOJI
from bot.constants.general import INTERVAL, WHITESPACE
from bot.modules.simple_client import SimpleClient


class ScheduledClient(SimpleClient):
    scheduler: BackgroundScheduler



    def get_unique_job_id(self, chat_id: int, module_name: str) -> str:
        return module_name + "_job_" + chat_id.__str__()

    def pause_job(self, chat_id: int, module_name: str):
        job: Job = self.scheduler.get_job(self.get_unique_job_id(chat_id, module_name))
        job.pause()


    def add_job_to_scheduler(self, chat_id: int, seconds: int, function: (), module_name: str, *args) -> Job:
        return self.scheduler.add_job(function,
                                      INTERVAL,
                                      seconds=seconds,
                                      id=self.get_unique_job_id(chat_id, module_name),
                                      replace_existing=True,
                                      args=[args[0], chat_id])

    def __init__(self, api_id, api_hash, bot_token):
        super().__init__(api_id, api_hash, bot_token)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    async def send_success_reply_message(self, incoming_message: Message, text: str, reply_markup: InlineKeyboardMarkup) -> Message:
        return await super().send_reply_message(incoming_message, CHECK_BOX_EMOJI + WHITESPACE + text,
                                                reply_markup)
