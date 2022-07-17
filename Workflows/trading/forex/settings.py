from Applications.TwelveDataTrading.references.dto import *


INDEX_ROOT_NAME_FOREX_AUTOCHARTIST_TRADER = 'FOREX_AUTOCHARTIST_TRADER'

traded_pairs = [
    'USDCAD',
    'USDJPY',
    'USDCHF',
    'AUDCAD',
    'AUDJPY',
    'AUDNZD',
    'AUDUSD',
    'BTCUSD',
    'CADCHF',
    'CADJPY',
    'CHFJPY',
    'EURAUD',
    'EURCAD',
    'EURAUD',
    'EURCHF',
    'EURGBP',
    'EURJPY',
    'EURNZD',
    'EURUSD',
    'GBPAUD',
    'GBPCAD',
    'GBPCHF',
    'GBPJPY',
    'GBPNZD',
    'GBPUSD',
    'NZDCAD',
    'NZDCHF',
    'NZDJPY',
    'NZDUSD',
    #'XAGUSD',
    #'XAUUSD',
    #'XCUUSD',
    #'XPTUSD',

]

except_pairs = [
    'XAGUSD',
    'XAUUSD',
    'XCUUSD',
    'XPTUSD',

]

traded_time_frames = {
    #1: "M1",
    #5: "M5",
    #15: "M15",
    60: "H1",
    240: "H4",
    1440: "DAILY",
    #10080: "WEEKLY"
}


traded_time_frames_indicator = {
    #1: "M1",
    #5: "M5",
    #15: "M15",
    60: EnumTimeframe.H1.value,
    240: EnumTimeframe.H4.value,
    1440: EnumTimeframe.DAILY.value,
    #10080: "WEEKLY"
}


str_card_title = """**{0}**[Pct: {1}  Entry: {2}  Stop: {3}  Target: {4}]"""

str_card_closed = """**{0}**[Pct: {1}  Entry: {2}  Stop: {3}  Target: {4}  P/L: {5}]"""

str_fx_add_card_description = """
#{0}

```
TRADE:
    signal_id: {1}
    trade_id: {2}
    lots: {3}
    score: {4}
```

![IMAGE]({5})

"""

str_fx_closed_card_description = """
```
CLOSED TRADE:
    price: {0}
    profit_loss: {1}
    trade_id: {2}
    fees: {3}
    closed: {4}
```
"""

str_autochartist_chart_url = "http://oanda.autochartist.com/aclite/imageViewer" \
                             "?type={0}&uid={1}&brokerid=320&w=315&h=200&offset=8"


str_indicators_values = """
```
INDICATORS:
    aots_current_indicator_value: {0}
    aots_trend_short_indicator_value: {1}
    aots_trend_long_indicator_value: {2}

```
"""
