import os
import socket
from datetime import datetime
from typing import List, Optional

import pytest
from pydantic import BaseModel

from foreverbull import broker
from foreverbull.broker.models.socket import SocketConfig
from foreverbull.worker import WorkerPool


class Environment(BaseModel):
    foreverbull_url: str = os.environ.get("FOREVERBULL_URL", "localhost:9000")
    strategy: str
    backtest_service: str
    backtest_ingestion: Optional[str]


class Configuration(BaseModel):
    symbols: List[str]
    benchmark: str
    calendar: str = "XNYS"
    start_time: datetime
    end_time: datetime


class Execution:
    def __init__(self):
        self._strategy = None
        self._worker_pool = None
        self._local_host = socket.gethostbyname(socket.gethostname())
        self._socket_config = SocketConfig()
        self._fb = None

    def setup(self, environment: Environment):
        self._strategy = broker.strategy.get(environment.strategy)
        if self._strategy is None:
            raise Exception("Strategy not found")
        self._worker_pool = WorkerPool()
        self._worker_pool.setup()
        self._socket_config.host = self._local_host
        self._socket_config.port = 5555

    def configure(self, configuration: Configuration):
        print("Configure: ", configuration)

    def run(self):
        print("Run")
        return None


@pytest.fixture(scope="function")
def execution():
    print("YES")
    execution = Execution()
    yield execution
    print("DONE")
