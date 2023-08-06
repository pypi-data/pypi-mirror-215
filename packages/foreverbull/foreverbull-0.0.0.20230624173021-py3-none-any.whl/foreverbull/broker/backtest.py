import requests

from foreverbull.models import Backtest

from .http import api_call


@api_call
def create(backtest: Backtest) -> requests.Request:
    return requests.Request(
        method="PUT",
        url="/api/v1/backtests",
        data=backtest.json(),
    )


@api_call
def get(backtest: str) -> requests.Request:
    return requests.Request(
        method="GET",
        url=f"/api/v1/backtests/{backtest}",
    )
