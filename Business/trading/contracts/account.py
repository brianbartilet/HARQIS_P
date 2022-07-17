from abc import abstractmethod
from Business.trading.models import *


class IAccount:

    @abstractmethod
    def get_account_summary(self, **kwargs) -> dict:
        ...

    @abstractmethod
    def get_orders(self, **kwargs) -> dict:
        ...

    @abstractmethod
    def get_portfolio_summary(self, **kwargs) -> dict:
        ...


