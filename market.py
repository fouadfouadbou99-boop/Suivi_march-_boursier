import numpy as np


def compute_metrics(df):

    close = df["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:,0]

    close = close.dropna()

    current_year = close.index[-1].year

    ytd = close[
        close.index.year == current_year
    ]

    perf_ytd = (
        close.iloc[-1]
        /
        ytd.iloc[0]
        -
        1
    ) * 100

    returns = close.pct_change().dropna()

    volatility = (
        returns.std()
        * np.sqrt(252)
        * 100
    )

    return {
        "Performance YTD": round(perf_ytd,2),
        "Volatilite": round(
