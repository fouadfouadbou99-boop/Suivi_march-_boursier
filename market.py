import pandas as pd
import numpy as np
import yfinance as yf


def load_yahoo_data(symbol):

    return yf.download(
        symbol,
        start="2020-01-01",
        auto_adjust=True,
        progress=False
    )


def load_maroc_index(filepath):

    df = pd.read_excel(filepath)

    df["Date"] = pd.to_datetime(df["Date"])

    df = df.sort_values("Date")

    df.set_index("Date", inplace=True)

    return df


def compute_metrics(df):

    close = df["Close"].dropna()

    current_year = close.index[-1].year

    ytd_data = close[
        close.index.year == current_year
    ]

    perf_ytd = (
        close.iloc[-1] /
        ytd_data.iloc[0] - 1
    ) * 100

    if len(close) >= 5:
        perf_1m = (
            close.iloc[-1] /
            close.iloc[-5] - 1
        ) * 100
    else:
        perf_1m = 0

    if len(close) >= 13:
        perf_3m = (
            close.iloc[-1] /
            close.iloc[-13] - 1
        ) * 100
    else:
        perf_3m = 0

    returns = close.pct_change().dropna()

    volatility = (
        returns.std()
        * np.sqrt(52)
        * 100
    )

    rolling_max = close.cummax()

    drawdown = (
        close - rolling_max
    ) / rolling_max

    max_drawdown = (
        drawdown.min() * 100
    )

    return {
        "Performance 1 mois (%)": round(perf_1m, 2),
        "Performance 3 mois (%)": round(perf_3m, 2),
        "Performance YTD (%)": round(perf_ytd, 2),
        "Volatilité (%)": round(volatility, 2),
        "Drawdown Max (%)": round(max_drawdown, 2)
    }


def generate_commentary(metrics):

    if metrics["Performance YTD (%)"] > 0:
        tendance = "haussière"
    else:
        tendance = "baissière"

    return (
        f"Performance YTD : {metrics['Performance YTD (%)']} %. "
        f"Performance 3 mois : {metrics['Performance 3 mois (%)']} %. "
        f"Volatilité : {metrics['Volatilité (%)']} %. "
        f"Drawdown max : {metrics['Drawdown Max (%)']} %. "
        f"Tendance : {tendance}."
    )
