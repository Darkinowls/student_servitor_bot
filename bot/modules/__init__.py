from bot.modules.basic_module import BasicModule
from bot.modules.scheduled_modules.gmail_module import GmailModule
from bot.modules.queue_module import QueueModule
from bot.modules.scheduled_modules.schedule_module import ScheduleClient
from bot import API_ID, BOT_NAME, API_HASH, BOT_TOKEN


class TelegramBot(
    GmailModule,
    QueueModule,
    ScheduleClient,
    BasicModule
):
    pass
    # def __init__(bot_name, api_id, api_hash, bot_token ):
    #     try:
    #         super().__init__(bot_name=BOT_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    #     except TelegramBotException as e:
    #


telegram_bot = TelegramBot(bot_name=BOT_NAME, api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
