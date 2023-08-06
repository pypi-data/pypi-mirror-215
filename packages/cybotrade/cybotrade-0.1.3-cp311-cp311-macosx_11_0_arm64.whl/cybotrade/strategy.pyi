from typing import List, Dict
from .models import (
    Candle,
    Performance,
    Interval,
)
from .runtime import StrategyTrader

import logging

class Strategy:
    """
    This class is a handler that will be used by the Runtime to handle events such as
    `on_candle_closed`, `on_order_update`, etc. The is a base class and every new strategy
    should be inheriting this class and override the methods.
    """

    logger = logging
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
        self,
        strategy: StrategyTrader,
        candle: Candle,
        candles: Dict[Interval, List[Candle]],
    ):
        """ """
    async def on_backtest_complete(
        self, strategy: StrategyTrader, performance: Performance
    ):
        """"""
