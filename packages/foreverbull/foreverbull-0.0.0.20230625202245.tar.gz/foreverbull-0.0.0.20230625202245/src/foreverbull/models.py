from datetime import datetime
from typing import List, Optional

from foreverbull.broker.models.base import Base
from foreverbull.broker.models.socket import SocketConfig
from foreverbull.broker.models.worker import Database


class Parameter(Base):
    key: str
    default: str = None
    value: str = None
    type: str


class Execution(Base):
    execution: str
    start_time: datetime
    end_time: datetime
    database: Optional[Database]
    parameters: Optional[List[Parameter]]
    socket: SocketConfig


class OHLC(Base):
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    time: datetime


class Info(Base):
    type: str
    version: str
    parameters: List[Parameter]
    routes: List[str]


class Backtest(Base):
    class Configuration(Base):
        start_time: datetime
        end_time: datetime
        symbols: List[str]

    backtest_service: str
    config: Configuration
    execution_type: str = "manual"
