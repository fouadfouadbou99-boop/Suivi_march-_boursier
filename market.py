import yfinance as yf
import pandas as pd
import numpy as np


def load_data(symbol, start="2020-01-01"):

    return yf.download(
        symbol,
        start=start,
        auto_adjust=True,
        progress=False
    )


def compute_metrics(df):

    if df.empty:
        return {
            "Performance YTD": 0.0,
            "Volatilite": 0.0
        }

    close = df["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    close = close.dropna()

    current_year = close.index[-1].year

    ytd_data = close[
        close.index.year == current_year
    ]

    first_value = float(ytd_data.iloc[0])

    last_value = float(close.iloc[-1])

    perf_ytd = (
        last_value / first_value
    ) - 1

    returns = close.pct_change().dropna()

    volatility = float(
        returns.std() * np.sqrt(252)
    )

    return {
        "Performance YTD": round(perf_ytd * 100, 2),
        "Volatilite": round(volatility * 100, 2)
    }


def generate_commentary(symbol, metrics):

    return (
        f"Indice {symbol} | "
        f"Performance YTD : {metrics['Performance YTD']}% | "
        f"Volatilité : {metrics['Volatilite']}%"
    )
