HELP_TITLE = "H"

SWAP_HELP = HELP_TITLE + "/swap 1 2\n" \
                         "Обмінює записи по індексам"

RM_HELP = HELP_TITLE + "/rm 1 2 .. 5\n" \
                       "Видаляє записи по індексам"

HEADER_HELP = HELP_TITLE + "/header 2га лаба\n" \
                           "Встановлює заголовок"

ADD_HELP = HELP_TITLE + "Виділіть чергу та пишіть"

ALL_COMMANDS = \
    """
Команди:
    
/queue або /q - Створює чергу

/gmail [gmail] [app-pass] - Створює з’єднання між цим чатом та gmail                       

/gmail - Надсилає адресу gmail, яку встановив користувач

/schedule [file.json] - Бере файл формату json і встановлює розклад для групи

/schedule - Повертає файл json, встановлений користувачем. Якщо його немає, надсилається приклад json   

/kpi_schedule - дозволяє обрати розклад з сайту schedule.kpi.ua       

/hi - Відповідає привіт

/week - Повідомляє номер поточного тижня

/help - Надсилає повідомлення з усіма командами
    """

# LABELS

HOW_TO_ADD = "Як додавати запис?"

HOW_TO_SET_HEADER = "Як встановити заголовок?"

HOW_TO_REMOVE = "Як видаляти запис?"

HOW_TO_SWAP = "Як переміщувати запиcи?"
