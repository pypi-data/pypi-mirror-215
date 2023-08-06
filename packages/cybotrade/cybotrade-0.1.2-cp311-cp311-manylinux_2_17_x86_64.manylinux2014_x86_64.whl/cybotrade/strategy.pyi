from typing import List
from cybotrade.models import (
    OrderParams,
    OrderResponse,
    Candle,
    Performance,
    RuntimeConfig,
)

import logging

class StrategyTrader:
    config: RuntimeConfig

    async def entry(self, params: OrderParams) -> OrderResponse:
        """
        Enters a trade with the given quantity, do note that this entry function will do
        pyramiding where it closes the existing position if one exists.
        """
    async def close_all(self):
        """
        Close all currently entered trades, do note that this function does not early exits even
        if it failed to close one of the trades, it will continue to close all orders.
        """
    async def performance(self):
        """
        Calculate and get the current performance of the running strategy.
        """

class Strategy:
    """
    This class is a handler that will be used by the Runtime to handle events such as
    `on_candle_closed`, `on_order_update`, etc. The is a base class and every new strategy
    should be inheriting this class and override the methods.
    """

    LOG_FORMAT: str

    def __init__(
        self,
        log_level: int = logging.INFO,
        handlers: List[logging.Handler] = [],
    ):
        """
        Set up the logger
        """
    async def on_candle_closed(
        self, strategy: StrategyTrader, candle: Candle, candles: List[Candle]
    ):
        """ """
    async def on_backtest_complete(
        self, strategy: StrategyTrader, performance: Performance
    ):
        """"""
