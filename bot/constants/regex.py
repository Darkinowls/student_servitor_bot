import re

GMAIL_REGEX = r"^[a-z0-9](\.?[a-z0-9]){5,}@gmail\.com$"

RECORD_REGEX = r'(([1-9])|(\d{2,}))?\.?\s*([a-zA-ZА-ЯҐЄІЇа-яґєії]{1,20}.*)'

END_LINE_BEHIND_REGEX = r'(?<=\n)'
END_AHEAD_REGEX = r'(?=\n|$)'

UTF_16_REGEX = r"\\u\d{3}\w"

LINK_REGEX: str = r"^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
TIME_REGEX: str = r"^([0-9])|([1][0-9])|(2[0-4])\.[0-6][0-9]$"

URL_BAD_SIGNS_REGEX = r"[^a-zA-ZА-ЯҐЄІЇа-яґєії0-9\s]*"

SWAP_REGEX = r"^\s*\d+\s+\d+\s*$"

GROUP_REGEX = r'^((ТІ)|(ТВ))-\d{2}[а-я]{0,2}$'