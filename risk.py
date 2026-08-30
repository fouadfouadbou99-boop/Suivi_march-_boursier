import numpy as np


def volatility(close):

    returns = close.pct_change().dropna()

    return (
        returns.std() *
        np.sqrt(252) *
        100
    )


def max_drawdown(close):

    rolling_max = close.cummax()

    drawdown = (
        close - rolling_max
    ) / rolling_max

    return drawdown.min() * 100
