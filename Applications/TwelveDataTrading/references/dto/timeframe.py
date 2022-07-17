from Core.web.api import *


class EnumTimeframe(Enum):
    M1 = '1min'
    M5 = '5min'
    M30 = '15min'
    M45 = '45min'
    H1 = '1h'
    H2 = '2h'
    H4 = '4h'
    DAILY = '1day'
    WEEKLY = '1week'
    MONTHLY = '1month'
