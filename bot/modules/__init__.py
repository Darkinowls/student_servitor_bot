from bot.modules.basic_module import BasicModule
from bot.modules.queue_module import QueueModule
from bot.modules.scheduled_modules.gmail_module import GmailModule
from bot.modules.scheduled_modules.schedule_module import ScheduleModule


class TelegramBot(
    ScheduleModule,
    GmailModule,
    QueueModule,
    BasicModule
):
    pass
