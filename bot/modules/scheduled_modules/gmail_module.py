from apscheduler.job import Job
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import filters
from pyrogram.types import Message

from bot.constants.database import CHAT_ID, APP_PASSWORD, GMAIL_ADDRESS, MODULE_IS_ON
from bot.constants.emoji import ENVELOPE_EMOJI
from bot.constants.general import WHITESPACE
from bot.constants.gmail import GMAIL, INTERVAL_SECS_GMAIL
from bot.database.gmail_session import GmailSession
from bot.decorators.on_message import on_message
from bot.email.gmail_client import GmailClient
from bot.exceptions.telegram_bot_error import TelegramBotError
from bot.helpers.gmail_helper import get_gmail_address_and_app_password_from_parameters
from bot.helpers.scheduler_helper import register_connection_switchers, create_keyboard_markup, get_turn_str
from bot.modules.scheduled_modules.scheduled_client import ScheduledClient


class GmailModule(ScheduledClient):
    scheduler: BackgroundScheduler

    def __send_on_schedule(self, *args: tuple[str, str] | int):
        gmail_address, app_password = args[0]
        chat_id: int = args[1]
        try:
            gmail_client = GmailClient(gmail_address, app_password)
            texts: list[str] = gmail_client.get_new_messages()
            for text in texts:
                self.send_message(chat_id=chat_id, text=ENVELOPE_EMOJI + WHITESPACE + text)
        except TelegramBotError as error:
            self.pause_job(chat_id, GMAIL)
            self.__gmail_sessions.set_session_module_is_on(chat_id, False)
            self.send_message(chat_id, error.__str__())

    def __add_previous_sessions_to_scheduler(self, gmail_session: GmailSession) -> BackgroundScheduler:

        for session in gmail_session.get_all_sessions():
            chat_id = int(session.get(CHAT_ID))
            app_password = session.get(APP_PASSWORD)
            gmail_address = session.get(GMAIL_ADDRESS)
            module_is_on = bool(session.get(MODULE_IS_ON))

            job: Job = self.add_job_to_scheduler(chat_id, INTERVAL_SECS_GMAIL, self.__send_on_schedule,
                                                 GMAIL, (gmail_address, app_password))
            if not module_is_on:
                job.pause()

        return self.scheduler

    def __init__(self, api_id, api_hash, bot_token):
        super().__init__(api_id, api_hash, bot_token)
        self.__gmail_sessions: GmailSession = GmailSession()
        self.__add_previous_sessions_to_scheduler(self.__gmail_sessions)
        register_connection_switchers(self, GMAIL, self.__gmail_sessions)

        @on_message(self, filters.regex("^/" + GMAIL + r"\s.*"))
        async def set_gmail_connection(_, message: Message):
            gmail_address, app_password = get_gmail_address_and_app_password_from_parameters(message.text)
            GmailClient(gmail_address, app_password)
            self.__gmail_sessions.upsert_session(message.chat.id, [gmail_address, app_password])
            self.add_job_to_scheduler(message.chat.id, INTERVAL_SECS_GMAIL, self.__send_on_schedule,
                                      GMAIL, (gmail_address, app_password))
            await self.send_success_reply_message(message,
                                                  "Gmail з'єднання встановлено успішно! Можете видалити це повідомлення",
                                                  create_keyboard_markup(GMAIL, "off"))

        @on_message(self, filters.command(GMAIL))
        async def send_my_gmail(_, message: Message):
            gmail_address_str, module_is_on = self.__gmail_sessions.get_session_and_module_is_on_by_chat_id(
                message.chat.id)
            if gmail_address_str is None:
                raise TelegramBotError("Ви ще не встановили gmail з'єднання.\n\n"
                                       "1. Як отримати app-pass: https://support.google.com/mail/answer/185833?hl=ru\n\n"
                                       "2. Як увімкнути IMAP: https://support.google.com/mail/answer/7126229?hl=ru\n\n"
                                       "3. Аби встановити це з'єднання використайте команду:\n"
                                       "/gmail [ваш gmail] [app-pass]"
                                       )
            await self.send_reply_message(message,
                                          "Ваш gmail адрес " + gmail_address_str,
                                          create_keyboard_markup(GMAIL, get_turn_str(not module_is_on)))
