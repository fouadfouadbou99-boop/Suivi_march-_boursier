import yfinance as yf
import pandas as pd


def load_yahoo_data(symbol):

    return yf.download(
        symbol,
        start="2020-01-01",
        auto_adjust=True,
        progress=False
    )


def load_maroc_index(path):

    df = pd.read_excel(path)

    df["Date"] = pd.to_datetime(df["Date"])

    df.set_index("Date", inplace=True)

    return df


def compute_performance(df):

    close = df["Close"]

    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    today = close.iloc[-1]

    ytd = close[
        close.index.year ==
        close.index[-1].year
    ]

    return {
        "Cours": today,
        "YTD": ((today / ytd.iloc[0]) - 1) * 100
    }
