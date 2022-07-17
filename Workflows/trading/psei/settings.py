import re
from datetime import datetime

DATETIME_FORMAT = datetime.today().strftime('%Y-%m-%d')
INDEX_ROOT_NAME_SCREENER = 'PSEI_SIGNALS_SCREENER'
INDEX_ROOT_NAME_TRADES = 'PSEI_TRADER'

str_stock_card_title = """**{0}**[Change: {1}  Last: {2}][{3}{4}][{5}]"""

str_stock_card_closed = """**{0}**[Pct: {1}  Entry: {2}  Stop: {3}  Target: {4}  P/L: {5}]"""

str_stock_card_title_strategy = """**{0}**[Change: {1}%  Last: {2}  Days: {3}  Total: {4}%][{5}{6}][{7}]"""

str_stock_card = """
#{0}

```
STOCK:
    last_price: {1}
    change_percent: {2}
    year_to_date: {3}
    open: {4}
    low: {5}
    high: {6}
```
"""

str_stock_trade_card = """
```
TRADE:
    id: {0}
    type: {1}
    price_entry: {2}
    price_stop: {3}
    price_profit: {4}
    risk_percent: {5}
    quantity: {6}
    sell_pending: {7}
    buy_pending: {8}
    gain_loss_percentage: {9}
    portfolio_percentage: {10}
    gain_loss_percentage_from_signal_date: {11}
```
"""


str_stock_indicators_card = """
```
INDICATORS:
    support_1: {0}
    support_2: {1}
    resistance_1: {2}
    resistance_2: {3}
    week_to_date: {4}
    month_to_date: {5}
    year_to_date: {6}
```
"""

str_stock_strategy_card = """
```
STRATEGY:
    name: {0}
    stock_name: {1}
    signal_date: {2}
    growth_percent_from_signal_date: {3}
    days_elapsed: {4}
    days_elapsed_to_stop: {5}
    days_elapsed_to_target: {6}
```
"""


def clean_percentage_values(clean_str: str):
    try:
        matches = re.search('\(([^)]+)', clean_str)
        value_str = clean_str
        if matches is not None:
            value_str = matches.group(1)
        ret = float(value_str.replace('%', ''))
    except:
        ret = clean_str
    return ret


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)