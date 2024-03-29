import unittest
from collections import OrderedDict

from bot.email.extracted_message import UNICODE_ESCAPE
from bot.helpers.datetime_helper import get_current_week_number, get_current_time_str, get_current_day_str
from bot.kpi_schedule.kpi_api import KpiRepo


class MyTestCase(unittest.TestCase):

    def test_utf_8(self):
        utf8_message = b"\xD0\xBF\xD1\x80\xD0\xB8\xD0\xB2\xD1\x96\xD1\x82".decode()
        self.assertEqual("привіт", utf8_message)

    def test_unicode_escape(self):
        utf16_message = '\\u0414\\u043e\\u0431\\u0440\\u043e\\u0433\\u043e \\u0432\\u0435\\u0447\\u0435\\u0440\\u0430'
        text = utf16_message.encode().decode(UNICODE_ESCAPE)
        print(text)
        self.assertEqual("Доброго вечера", text)

    def test_get_current_datetime(self):
        week_num: int = get_current_week_number()
        day_str: str = get_current_day_str()
        time_str: str = get_current_time_str()
        print(week_num, day_str, time_str)

    def test_str(self):
        KpiRepo().downloadGroups()



    def test_bool(self):
        print(True)

    def test_OrderedDict(self):
        self.assertEqual([], list(OrderedDict({0: "amogus"})))


if __name__ == '__main__':
    unittest.main()
