import imaplib

from imbox import Imbox

from bot.constants.gmail import IMAP_GMAIL_SERVER
from bot.email.extracted_message import ExtractedMessage
from bot.exceptions.telegram_bot_error import TelegramBotError


class GmailClient:
    __email_address: str
    __password: str

    def __init__(self, email_address: str, password: str):
        self.__email_address = email_address
        self.__password = password
        self.__create_imbox()

    def get_new_messages(self) -> list[str]:
        texts: list[str] = []
        imbox = self.__create_imbox()
        raw_messages: list = imbox.messages(unread=True)
        for uid, message in raw_messages[:2]:
            e_message = ExtractedMessage(message)
            texts.append(e_message.__str__())
            imbox.mark_seen(uid)
        return texts

    def __create_imbox(self):
        try:
            return Imbox(IMAP_GMAIL_SERVER, username=self.__email_address, password=self.__password)
        except imaplib.IMAP4.error:
            raise TelegramBotError('Аутентифікація провалилася.\n'
                                   'Будь-ласка перегляньте документацію')
