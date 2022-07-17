from Business.trading.models import *


class OrderStatusAAA(Enum):
    PENDING_TRIGGER = 'Pending Trigger'
    QUEUED = 'Queued'
    FILLED = 'Filled'


class ConditionsOrderFieldAAA(Enum):
    LAST_PRICE = 'Last Price'
    NONE = 'None'


class ConditionsOrderTriggerAAA(Enum):
    GREATER_THAN_OR_EQUAL_TO = 'Greater Than Or Equal'
    LESS_THAN_OR_EQUAL_TO = 'Less Than Or equal'
    EQUAL = 'Equal'


class DtoCreateOrderAAA(JsonObject):
    stock_name = str
    transaction = Order.BUY.value

    order_type = OrderType.LIMIT.value
    quantity = int
    good_until = OrderValidUntil.GTC.value
    price = float

    condition_field = ConditionsOrderFieldAAA.NONE.value
    condition_price = float
    condition_trigger = ConditionsOrderTriggerAAA.EQUAL.value
    condition_expiry_date = None  # MM/DD/YYYY

    created = False
    order_value = float
    total_fees = float
    net_value = float


class DtoOrderAAA(DtoCreateOrderAAA):
    id = str
    status = int
    filled_quantity = int
    pending_quantity = int
    average_price = float
    order_value = float
    net_value = float
    order_date = str
    condition_order_id = int
    exchange = str
    distance = float


