from bot.constants.emoji import RED_CROSS_EMOJI
from bot.constants.general import WHITESPACE


class TelegramBotException(Exception):

    def __init__(self, text):
        self.__text = RED_CROSS_EMOJI + WHITESPACE + text
        super().__init__(self.__text)

    def __str__(self):
        return self.__text
